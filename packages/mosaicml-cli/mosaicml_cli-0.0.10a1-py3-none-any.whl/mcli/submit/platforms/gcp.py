""" The GCP Platform """
from dataclasses import dataclass
from typing import Dict, Optional

from mcli.submit.platforms.gcp_instances import GCP_INSTANCE_LIST
from mcli.submit.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.submit.platforms.platform import Platform

TF_VERSION = '2.6.0'
PYTORCH_TPU_ENV = 'tpu_worker;0;${KUBE_GOOGLE_CLOUD_TPU_ENDPOINTS:7}'  # noqa: W605


@dataclass
class GCPPlatform(Platform):
    """ The GCP Platform """

    allowed_instances: InstanceList = GCP_INSTANCE_LIST

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
        if instance.gpu_count is not None and instance.gpu_count > 0:
            if instance.gpu_type == GPUType.TPUv2:
                limits['cloud-tpus.google.com/v2'] = instance.gpu_count
            elif instance.gpu_type == GPUType.TPUv3:
                limits['cloud-tpus.google.com/v3'] = instance.gpu_count
            else:
                limits['nvidia.com/gpu'] = instance.gpu_count

        requests['cpu'] = instance.cpu_count - 1  # -1 core for buffer
        limits['cpu'] = instance.cpu_count

        return {'requests': requests, 'limits': limits}

    def get_node_selector(self, instance_type: str) -> Dict[str, str]:
        """ GCP uses a special resource for the instance type
        """
        instance = self.get_instance(instance_type=instance_type)
        node_class = instance.node_class
        return {'mosaicml.com/node-class': node_class}

    def get_annotations(self, instance_type: str):
        instance = self.get_instance(instance_type=instance_type)
        if instance.gpu_type in (GPUType.TPUv2, GPUType.TPUv3):
            return {'tf-version.cloud-tpus.google.com': TF_VERSION}
        else:
            return {}

    def get_setup_command(self, instance_type: str) -> Optional[str]:
        instance = self.get_instance(instance_type=instance_type)
        if instance.gpu_type in (GPUType.TPUv2, GPUType.TPUv3):
            return f'export XRT_TPU_CONFIG="{PYTORCH_TPU_ENV}"'
        else:
            return None
