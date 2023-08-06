""" The COTA Platform """
from dataclasses import dataclass
from typing import Dict

from kubernetes import client

from mcli.submit.platforms.cota_instances import COTA_INSTANCE_LIST
from mcli.submit.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.submit.platforms.platform import Platform

NUM_MULTI_GPU_TOLERATE = 8
MAX_CPUS = 120


@dataclass
class COTAPlatform(Platform):
    """ The COTA Platform """

    allowed_instances: InstanceList = COTA_INSTANCE_LIST

    def __post_init__(self):
        self.pvc_datasets_name = f'{self.pvc_name}-datasets'

    def get_node_selector(self, instance_type: str):
        instance = self.get_instance(instance_type=instance_type)
        selectors = {}
        if instance.is_gpu:
            if instance.gpu_type == GPUType.RTX3080:
                node_class = 'mml-nv3080'
            elif instance.gpu_type == GPUType.RTX3090:
                node_class = 'mml-nv3090'
            else:
                raise KeyError('Unknown node class')
            selectors.update({'mosaicml.com/node-class': node_class})

        if instance.is_gpu and instance.gpu_count == NUM_MULTI_GPU_TOLERATE:
            selectors.update({f'mosaicml.com/multigpu_{NUM_MULTI_GPU_TOLERATE}': 'true'})
        return selectors

    def get_resources(self, instance_type: str) -> Dict[str, Dict[str, int]]:
        """
        Returns resource requests and limits for kubernetes.
        """
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)

        if instance is None:
            raise ValueError(f'{instance_type} not found in GCP')

        assert isinstance(instance, InstanceType)

        requests: Dict[str, int] = {}
        limits: Dict[str, int] = {}
        if instance.is_gpu:
            assert isinstance(instance.gpu_count, int)
            limits['nvidia.com/gpu'] = instance.gpu_count

        requests['cpu'] = instance.cpu_count - 1  # -1 core for buffer
        limits['cpu'] = instance.cpu_count

        assert instance.cpu_count <= MAX_CPUS, ('The chosen number of cpus: '
                                                f'{instance.cpu_count} is greater than the max {MAX_CPUS}')
        return {'requests': requests, 'limits': limits}

    def get_volume_mounts(self):
        # NOTE: workdisk will be obsoleted soon!
        return [
            client.V1VolumeMount(name='dshm', mount_path='/dev/shm'),
            client.V1VolumeMount(name='workdisk', mount_path=self.mount_path),
            client.V1VolumeMount(name='local', mount_path='/localdisk')
        ]

    def get_volumes(self):
        # NOTE: workdisk and local will be obsoleted soon!
        return [
            client.V1Volume(name='dshm', empty_dir=client.V1EmptyDirVolumeSource(medium='Memory')),
            client.V1Volume(
                name='workdisk',
                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name=self.pvc_name)),
            client.V1Volume(name='local', host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'))
        ]

    def get_tolerations(self, instance_type: str):
        tolerations = []
        resources = self.get_resources(instance_type)
        num_gpus = resources['limits'].get('nvidia.com/gpu', 0)

        if num_gpus > 0:
            tolerations.append({
                'effect': 'PreferNoSchedule',
                'key': 'mosaicml.com/prefer-gpu-workloads',
                'operator': 'Equal',
                'value': 'true'
            })

        if num_gpus == NUM_MULTI_GPU_TOLERATE:
            tolerations.append({
                'effect': 'NoSchedule',
                'key': f'mosaicml.com/multigpu_{NUM_MULTI_GPU_TOLERATE}',
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations
