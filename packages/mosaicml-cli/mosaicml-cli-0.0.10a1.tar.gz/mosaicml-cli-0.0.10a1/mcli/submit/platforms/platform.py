""" The base class for how a platform will operate """
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kubernetes import client
from kubernetes import config as kubectl_get_contexts

from mcli import config
from mcli.submit.kubernetes import utils
from mcli.submit.platforms.instance_type import InstanceList, InstanceType

# types
Resources = Dict[str, int]
Description = Dict[str, Any]


@dataclass
class Platform(ABC):
    """ Base class for platforms."""

    context_name: str  # used to switch platforms in kubeconfig. See kubectl config get-contexts
    namespace: str  # namespace, typically your name
    mount_path: str  # the pvc is mounted to this path inside docker
    dataset_path: str  # path to training datasets inside docker, must be on a valid mounted volume
    pvc_name: str  # persistent volume claim to shared storage. used for datasets and artifacts
    allowed_instances: InstanceList  # InstanceList

    image_pull_secrets: Optional[str] = None  # optional name of the docker secret in kubectl secrets

    ssh_secrets: Optional[str] = None  # optional ssh-key secret
    ssh_secrets_mount_path: Optional[str] = None  # optional path to secrets mount

    mosaicdb_secrets: Optional[str] = None
    mosaicdb_secrets_mount_path: Optional[str] = None

    # TODO(TL): Default set here because it's not set in mosaic config.
    wandb_secret: Optional[str] = 'wandb'  # Optional WandB API key secret.
    wandb_secret_data_key: Optional[str] = 'value'  # Optional key within ``wandb_secret`` to look for the WandB key

    ebs_path: Optional[str] = None  # path to EBS mount. None if not supported.

    # priority class to use for the job
    priority_class_labels = {}  # type: Dict[str, str]
    default_priority_class: Optional[str] = None  # If a priority class should be default, put it here.

    def __post_init__(self):
        required_fields = ['context_name', 'namespace', 'mount_path', 'dataset_path']

        for _field in required_fields:
            if not hasattr(self, _field):
                raise ValueError(f'Missing field in mosaic config: {_field}')

        self._check_context_name()

    def _check_context_name(self):
        """ check the context name is in the kubernetes config """
        contexts: List[Dict[str, str]]
        contexts, _ = kubectl_get_contexts.list_kube_config_contexts(os.environ.get('KUBECONFIG'))  # type: ignore
        if not contexts:
            raise ValueError('Contexts not found in kube config.')

        context_names = [context['name'] for context in contexts]
        if self.context_name not in context_names:
            raise ValueError(f'Context {self.context_name} not found.  Available contexts: {contexts}')

    def get_node_selector(self, instance_type: str) -> Dict[str, str]:
        return {'beta.kubernetes.io/instance-type': instance_type}

    def get_annotations(self, instance_type: str):
        del instance_type
        return {}

    def is_allowed_instance(self, instance_type: str) -> bool:
        """ checks if the instance type is an allowed instances """
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)
        if instance is None:
            return False
        return True

    def get_instance(self, instance_type: str) -> InstanceType:
        """ gets the InstanceType from a str, throws if not available in platform"""
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)
        if instance is None:
            raise ValueError(f'{instance_type} not found in {self.__class__.__name__}')
        assert isinstance(instance, InstanceType)
        return instance

    def get_instance_description(self, instance_type: str) -> str:
        instance = self.get_instance(instance_type=instance_type)
        return instance.desc

    def get_smallest_cpu_instance(self, min_cpus: int) -> InstanceType:
        assert min_cpus > 0, f'min_cpus must be > 0, got {min_cpus}.'
        min_instance = None
        available_cpus = float('inf')

        for instance in self.allowed_instances:
            if (instance.gpu_count is None or instance.gpu_count == 0) and \
              (instance.cpu_count is not None and  0 < instance.cpu_count < available_cpus):
                min_instance = instance
                available_cpus = instance.cpu_count

        if min_instance is None:
            raise ValueError(f'CPU-only node on {self.context_name} '
                             f'with at least {min_cpus} cpus not found.'
                             ' Use benchmark instances to view available types.')
        assert min_instance is not None
        print(min_instance)
        return min_instance

    def get_volume_mounts(self):
        # NOTE: workdisk will be obsoleted soon!
        return [
            client.V1VolumeMount(name='dshm', mount_path='/dev/shm'),
            client.V1VolumeMount(name='workdisk', mount_path=self.mount_path)
        ]

    def get_volumes(self):
        # NOTE: workdisk will be obsoleted soon!
        return [
            client.V1Volume(name='dshm', empty_dir=client.V1EmptyDirVolumeSource(medium='Memory')),
            client.V1Volume(
                name='workdisk',
                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=self.pvc_name)),
        ]

    def get_setup_command(self, instance_type: str) -> Optional[str]:
        """ returns any platform-specific setup commands. These setup commands
        are prepended to the user-provided command. Defaults to None.
        """
        del instance_type

    def get_tolerations(self, instance_type: str):
        del instance_type
        return []

    def get_ebs_pvc(self, pvc_name: Optional[str] = None):
        assert pvc_name is None, 'EBS PVC not supported for this platform.'
        return {}

    def get_specs(self, instance_type: str, attach_ebs: bool = False, priority_class: Optional[str] = None):
        """
        Generates base kubernetes specs

        Arguments:
            instance_type (str): Name of the instance.
            attach_ebs (bool): If ``True``, attempt to attach an EBS volume if one is available. Default ``False``.
            priority_class (Optional[str]): Priority at which the job should run. Must be one of the priorities
                                            specified by the platform.
        """
        other_specs = []

        # Create base job spec
        job_spec = client.V1Job(api_version='batch/v1', kind='Job')
        job_spec.metadata = client.V1ObjectMeta(namespace=self.namespace,
                                                name='default',
                                                annotations=self.get_annotations(instance_type))
        job_spec.status = client.V1JobStatus()

        env_vars = {
            'MOSAICML_INSTANCE_TYPE': instance_type,
            'MOSAICML_DATASET_PATH': self.dataset_path,
            'MOSAICML_MOUNT_PATH': self.mount_path
        }

        instance = self.get_instance(instance_type)
        # Add LOCAL_WORLD_SIZE env var to represent number of GPUs on the instance
        if instance.gpu_count is not None and instance.gpu_count > 0:
            env_vars['LOCAL_WORLD_SIZE'] = str(instance.gpu_count)

        resources = self.get_resources(instance_type)
        # If no GPUs requested, limit the container visibility with this envvar.
        # see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#gpu-enumeration
        if resources['limits'].get('nvidia.com/gpu', 0) == 0:
            env_vars['NVIDIA_VISIBLE_DEVICES'] = 'void'

        volumes = self.get_volumes()
        volume_mounts = self.get_volume_mounts()

        if self.image_pull_secrets is not None:
            image_pull_secrets = [client.V1LocalObjectReference(name=self.image_pull_secrets)]
        else:
            image_pull_secrets = None

        # TODO(Niklas): Consider moving this to user, or job abstraction.
        if self.ssh_secrets is not None and self.ssh_secrets_mount_path is not None:
            volumes.append(
                client.V1Volume(
                    name='secret-ssh-volume',
                    secret=client.V1SecretVolumeSource(default_mode=256, secret_name=self.ssh_secrets),
                ))
            volume_mounts.append(
                client.V1VolumeMount(
                    name='secret-ssh-volume',
                    mount_path=self.ssh_secrets_mount_path,
                    read_only=True,
                ))
            key_name: str = 'ssh-privatekey'
            if config.feature_enabled(config.FeatureFlag.DEPRECATED_SSH_KEY):
                key_name = 'ssh_private_key'
            env_vars['GIT_SSH_COMMAND'] = f'ssh -i {self.ssh_secrets_mount_path}/{key_name}'

        # TODO(Niklas): Issue warning if ebs_path is not available.
        if attach_ebs and self.ebs_path is not None:
            pvc_name = f'pvc-{utils.generate_uuid()}'

            other_specs.append(self.get_ebs_pvc(pvc_name=pvc_name))
            volumes.append(
                client.V1Volume(
                    name='ebs',
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=pvc_name),
                ))
            volume_mounts.append(client.V1VolumeMount(name='ebs', mount_path=self.ebs_path))

        # Update to default priority class for the platform
        if priority_class is None:
            priority_class = self.default_priority_class

        # Error if priority class is unknown
        if priority_class is not None:
            if priority_class not in self.priority_class_labels:
                raise ValueError(
                    f'Invalid priority class. Must be one of {self.priority_class_labels}, not {priority_class}')
            priority_class_label = self.priority_class_labels[priority_class]
        else:
            priority_class_label = None

        env_list = []
        for env_name, env_value in env_vars.items():
            env_list.append(client.V1EnvVar(name=env_name, value=env_value))

        # TODO(TL): Also may be moved to a different user/job abstraction
        if self.wandb_secret is not None:
            wandb_secret_key = self.wandb_secret_data_key
            if config.feature_enabled(config.FeatureFlag.DEPRECATED_WANDB_KEY):
                wandb_secret_key = 'wandb_api_key'
            wandb_env = client.V1EnvVar(name='WANDB_API_KEY',
                                        value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(
                                            name=self.wandb_secret, key=wandb_secret_key, optional=True)))
            env_list.append(wandb_env)

        container = client.V1Container(name='default', env=env_list, resources=resources, volume_mounts=volume_mounts)

        template = client.V1PodTemplate()
        template.template = client.V1PodTemplateSpec()
        template.template.spec = client.V1PodSpec(containers=[container],
                                                  volumes=volumes,
                                                  restart_policy='Never',
                                                  tolerations=self.get_tolerations(instance_type),
                                                  host_ipc=True,
                                                  node_selector=self.get_node_selector(instance_type),
                                                  image_pull_secrets=image_pull_secrets,
                                                  priority_class_name=priority_class_label)

        template.template.metadata = client.V1ObjectMeta(annotations=self.get_annotations(instance_type))
        job_spec.spec = client.V1JobSpec(template=template.template, backoff_limit=0)

        # Create shared metadata
        shared_metadata = client.V1ObjectMeta(namespace=self.namespace, labels={'mosaicml.com/instance': instance_type})

        return [job_spec, other_specs, shared_metadata]

    @abstractmethod
    def get_resources(self, instance_type: str) -> Dict[str, Dict[str, int]]:
        """ returns the resources needed for kubernetes requests, in the format:
        {requests:.., limits:...}. """
        raise NotImplementedError
