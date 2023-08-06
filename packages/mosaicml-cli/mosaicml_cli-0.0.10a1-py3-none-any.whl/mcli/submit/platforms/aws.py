""" The AWS Platform """
from dataclasses import dataclass
from typing import Dict

from mcli.submit.platforms.aws_instances import AWS_INSTANCE_LIST
from mcli.submit.platforms.instance_type import InstanceList, InstanceType
from mcli.submit.platforms.platform import Platform
from mcli.submit.platforms.volumekind import VolumeKind


@dataclass
class AWSPlatform(Platform):
    """ The AWS Platform """

    ebs_path: str = '/mnt/ebs'  # TODO: move to config

    allowed_instances: InstanceList = AWS_INSTANCE_LIST
    resources = {}

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

    def get_ebs_pvc(self, pvc_name='ebs-pvc'):
        # TODO: this is a temporary hack
        # TODO(Niklas): Use python Kubernetes SDK
        pvc_body = {
            'api_version': 'v1',
            'kind': 'PersistentVolumeClaim',
            'metadata': {
                'name': pvc_name,
                'labels': {
                    'type': 'ebs'
                }
            },
            'spec': {
                'accessModes': ['ReadWriteOnce'],
                'storageClassName': 'ebs-sc',
                'dataSource': {
                    'name': 'dataset-imagenet-snap',
                    'kind': 'VolumeSnapshot',
                    'apiGroup': 'snapshot.storage.k8s.io'
                },
                'resources': {
                    'requests': {
                        'storage': '200Gi'
                    }
                }
            }
        }

        return pvc_body

    def get_ebs_volume(self, claim_name='ebs-pvc'):
        return {
            'name': 'ebs-pvc',
            'mount_path': self.ebs_path,
            'volume_kind': VolumeKind.PERSISTENT_VOLUME_CLAIM,
            'volume_kwargs': {
                'claim_name': claim_name
            }
        }
