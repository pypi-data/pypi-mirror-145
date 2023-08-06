""" The Azure Platform """
from dataclasses import dataclass
from typing import Dict

from mcli.submit.platforms.azure_instances import AZURE_INSTANCE_LIST
from mcli.submit.platforms.instance_type import InstanceList, InstanceType
from mcli.submit.platforms.platform import Platform


@dataclass
class AzurePlatform(Platform):
    """ The Azure Platform """

    allowed_instances: InstanceList = AZURE_INSTANCE_LIST

    def get_resources(self, instance_type: str) -> Dict[str, Dict[str, int]]:
        """
        Returns resource requests and limits for kubernetes. Resources are
        hard-coded.
        """

        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)

        if instance is None:
            raise ValueError(f'{instance_type} not found in AWS')

        assert isinstance(instance, InstanceType)
        requests: Dict[str, int] = {}
        limits: Dict[str, int] = {}
        if instance.gpu_count is not None and instance.gpu_count > 0:
            limits['nvidia.com/gpu'] = instance.gpu_count

        requests['cpu'] = instance.cpu_count - 1  # -1 core for buffer
        limits['cpu'] = instance.cpu_count

        return {'requests': requests, 'limits': limits}
