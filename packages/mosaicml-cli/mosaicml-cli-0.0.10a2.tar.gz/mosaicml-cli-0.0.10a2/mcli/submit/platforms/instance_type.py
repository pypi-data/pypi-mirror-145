""" The InstanceType Abstraction for different instance configs """
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Set

import yaml


class GPUType(Enum):
    """ The Type of GPU to use in a job """
    NONE = 'none'
    A100 = 'A100'
    V100 = 'V100'
    P100 = 'P100'
    T4 = 'T4'
    K80 = 'K80'
    RTX3080 = '3080'
    RTX3090 = '3090'
    TPUv2 = 'TPUv2'  # pylint: disable=invalid-name
    TPUv3 = 'TPUv3'  # pylint: disable=invalid-name


@dataclass
class InstanceType():
    """ The InstanceType Abstraction for different instance configs """
    name: str
    desc: str
    cpu_count: int
    gpu_count: Optional[int]
    gpu_type: GPUType = GPUType.NONE
    gpu_memory: Optional[int] = None
    extras: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        data = asdict(self)
        data['gpu_type'] = data['gpu_type'].value
        return yaml.dump(data)

    def __gt__(self, other):
        return self.name < other.name

    @property
    def node_class(self) -> str:
        """ Retrieves the node_class if set in extras,
        otherwise falls back to instance_type.name
        """
        return self.extras.get('node_class', self.name)

    @property
    def is_gpu(self) -> bool:
        return self.gpu_count is not None and self.gpu_count > 0


class InstanceList():
    """ An abstraction over a platforms available instance types """

    def __init__(self, instances: List[InstanceType]) -> None:
        self.instances = instances

    def get_allowed_instances(self) -> Set[str]:
        return {i.name for i in self.instances}

    def get_instance_by_name(self, instance_name: str) -> Optional[InstanceType]:
        for inst in self.instances:
            if inst.name == instance_name:
                return inst
        return None

    def __iter__(self) -> Iterator[InstanceType]:
        """ allow iteration through the instances"""
        return iter(self.instances)
