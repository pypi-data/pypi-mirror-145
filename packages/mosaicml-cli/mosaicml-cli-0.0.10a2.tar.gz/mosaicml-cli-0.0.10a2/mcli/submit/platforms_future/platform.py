# pylint: disable=duplicate-code

""" The base class for how a platform will operate """
from abc import ABC
from typing import Any, Dict, List, Optional

from kubernetes import client

from mcli.config_objects import MCLIPlatform
from mcli.submit.kubernetes.mcli_job_future import MCLIK8sJob, MCLIVolume
from mcli.submit.platforms_future.experimental import ExperimentalFlag, PlatformExperimental
from mcli.submit.platforms_future.instance_type import InstanceList, InstanceType
from mcli.utils.utils_kube import safe_update_optional_dictionary, safe_update_optional_list
from mcli.utils.utils_kube_labels import label

# types
Resources = Dict[str, int]
Description = Dict[str, Any]


class PlatformInstance(ABC):
    """ All Instance Related Functions """
    allowed_instances: InstanceList  # InstanceList

    def is_allowed_instance(self, instance_type: InstanceType) -> bool:
        """ checks if the instance type is an allowed instances """
        return self.allowed_instances.is_allowed_instance_type(instance_type=instance_type)

    def get_instance(self, instance_type: str) -> InstanceType:
        """ gets the InstanceType from a str, throws if not available in platform"""
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)
        if instance is None:
            raise ValueError(f'{instance_type} not found in {self.__class__.__name__}')
        assert isinstance(instance, InstanceType)
        return instance


class PlatformPriority(ABC):
    # priority class to use for the job
    priority_class_labels: Dict[str, str] = {}
    default_priority_class: Optional[str] = None  # If a priority class should be default, put it here.

    def get_priority_class_label(self, priority_class_override: Optional[str]) -> Optional[str]:
        priority_class = priority_class_override if priority_class_override else self.default_priority_class
        priority_class_label: Optional[str] = None
        if priority_class is not None:
            if priority_class not in self.priority_class_labels:
                raise ValueError(
                    f'Invalid priority class. Must be one of {self.priority_class_labels}, not {priority_class}')
            priority_class_label = self.priority_class_labels[priority_class]
        return priority_class_label


class PlatformProperties(ABC):
    platform_information: MCLIPlatform

    @property
    def namespace(self):
        return self.platform_information.namespace


class GenericK8sPlatform(PlatformInstance, PlatformPriority, PlatformProperties, PlatformExperimental):
    """ A Generic Platform implementation """

    def __init__(self, platform_information: MCLIPlatform) -> None:
        self.platform_information = platform_information
        super().__init__()

    def get_node_selectors(self, instance_type: InstanceType) -> Dict[str, str]:
        # Possibly add multi-node selectors here
        return instance_type.node_selectors

    def get_annotations(self, instance_type: InstanceType):
        del instance_type
        return {}

    def get_volumes(self) -> List[MCLIVolume]:
        return [
            MCLIVolume(
                volume=client.V1Volume(
                    name='dshm',
                    empty_dir=client.V1EmptyDirVolumeSource(medium='Memory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='dshm',
                    mount_path='/dev/shm',
                ),
            ),
        ]

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        return []

    def prepare_job_for_platform(
        self,
        job_spec: MCLIK8sJob,
        instance_type: InstanceType,
        priority_class: Optional[str] = None,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
    ) -> None:
        """Modifies a MCLIK8sJob with the proper specs of the Platform

        Args:
            job_spec: The MCLIK8sJob object to that represents the K8s job
            instance_type: The instance type to use on the platform
            priority_class: An optional priority class to assign the job to
            experimental_flags: A list of experimental flags to enable,
                if the instance allows them. Defaults to None.
        """
        if experimental_flags is None:
            experimental_flags = []

        job_spec.metadata.namespace = self.namespace
        job_spec.metadata.annotations = self.get_annotations(instance_type)
        job_spec.spec.backoff_limit = 0

        env_vars = {'MOSAICML_INSTANCE_TYPE': instance_type.name}

        # Add LOCAL_WORLD_SIZE env var to represent number of GPUs on the instance
        if instance_type.gpu_count is not None and instance_type.gpu_count > 0:
            env_vars['LOCAL_WORLD_SIZE'] = str(instance_type.gpu_count)

        resources = instance_type.resource_requirements
        job_spec.container.resources = resources

        if isinstance(resources.limits, dict) and \
           resources.limits.get(label.nvidia.GPU, 0) == 0:
            # If no GPUs requested, limit the container visibility with this envvar.
            # see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#gpu-enumeration
            env_vars['NVIDIA_VISIBLE_DEVICES'] = 'void'  # type: ignore

        volumes = self.get_volumes()
        for volume in volumes:
            job_spec.add_volume(volume)

        pod_spec = job_spec.pod_spec
        pod_spec.priority_class_name = self.get_priority_class_label(priority_class_override=priority_class)
        for env_name, env_value in env_vars.items():
            job_spec.add_environment_variable(client.V1EnvVar(
                name=env_name,
                value=env_value,
            ))

        pod_spec.restart_policy = 'Never'
        pod_spec.host_ipc = True
        pod_spec.tolerations = safe_update_optional_list(
            pod_spec.tolerations,
            self.get_tolerations(instance_type),
        )
        pod_spec.node_selector = safe_update_optional_dictionary(
            pod_spec.node_selector,
            self.get_node_selectors(instance_type),
        )

        # Apply optional experimental flags
        self.apply_experimental_flags(
            job_spec=job_spec,
            instance=instance_type,
            experimental_flags=experimental_flags,
        )

    def get_shared_metadata(self, instance_type: InstanceType) -> client.V1ObjectMeta:
        return client.V1ObjectMeta(
            namespace=self.namespace,
            labels={
                label.mosaic.LABEL_INSTANCE: instance_type.name,
            },
        )
