""" R1Z! Platform Definition """
from dataclasses import dataclass
from typing import Dict

from kubernetes import client

from mcli.submit.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.submit.platforms.platform import Platform
from mcli.submit.platforms.r6z1_instances import R6Z1_INSTANCE_LIST

NUM_MULTI_GPU_TOLERATE = 8
MAX_CPUS = 60

R6Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


@dataclass
class R6Z1Platform(Platform):
    """ R6Z1 Platform Overrides """

    allowed_instances: InstanceList = R6Z1_INSTANCE_LIST
    priority_class_labels = R6Z1_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'

    def __post_init__(self):
        self.pvc_datasets_name = f'{self.pvc_name}-datasets'

    def get_node_selector(self, instance_type: str):
        instance = self.get_instance(instance_type=instance_type)
        selectors = {}
        if instance.is_gpu:
            if instance.gpu_type == GPUType.A100:
                node_class = 'a100-40sxm'
            else:
                raise KeyError('Unknown node class')
            selectors.update({'mosaicml.com/node-class': node_class})

        return selectors

    def get_resources(self, instance_type: str) -> Dict[str, Dict[str, int]]:
        """
        Returns resource requests and limits for kubernetes.
        """
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)

        if instance is None:
            raise ValueError(f'{instance_type} not found in r6z1')

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
        return [
            client.V1VolumeMount(name='dshm', mount_path='/dev/shm'),
        ]

    def get_volumes(self):
        return [
            client.V1Volume(name='dshm', empty_dir=client.V1EmptyDirVolumeSource(medium='Memory')),
        ]

    def get_tolerations(self, instance_type: str):
        return []
