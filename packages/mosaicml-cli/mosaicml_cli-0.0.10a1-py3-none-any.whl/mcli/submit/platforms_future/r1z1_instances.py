# pylint: disable=duplicate-code

""" Available Instances for the R1Z1 Platform """
import re
from typing import List, Optional, Set

from mcli.submit.platforms_future.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 7
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='r1z1-g1-a100',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='1x a100s',
    ),
    InstanceType(
        name='r1z1-g2-a100',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='2x a100s',
    ),
    InstanceType(
        name='r1z1-g4-a100',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='4x a100s',
    ),
    InstanceType(
        name='r1z1-g8-a100',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='8x a100s',
    ),
]


def add_node_selector_to_instance(instance: InstanceType) -> None:
    instance.extras.update({'node_selector': label.mosaic.NODE_CLASS})

    if instance.gpu_type == GPUType.A100:
        instance.extras.update({'node_class': 'a100-80sxm'})


for r1z1_instance in ALLOWED_INSTANCES:
    add_node_selector_to_instance(r1z1_instance)

valid_r1z1_regex_configs = [
    'r1z1-g[1-8]-a100$',
    r'r1z1-g[1-8]-c[1-9]\d?\d?-a100',  # type: ignore
]


class R1Z1InstanceList(InstanceList):
    """ Available Instances for the R1Z1 Platform """

    def __init__(self, instances: List[InstanceType]) -> None:
        super().__init__(instances=instances)

    def get_allowed_instances(self) -> Set[str]:
        return {i.name for i in self.instances}

    def get_instance_by_name(self, instance_name: str) -> Optional[InstanceType]:
        for inst in self.instances:
            if inst.name == instance_name:
                return inst

        if any((re.match(x, instance_name) for x in valid_r1z1_regex_configs)):
            print(f'Matched: {instance_name}')
            items = instance_name.split('-')[1:]
            gpu_enabled = any(('g' in x for x in items))
            cpu_count = 0
            gpu_count = 0
            if gpu_enabled:
                gpu_count = int([x for x in items if 'g' in x][0][1:])
                cpu_item = [x for x in items if 'c' in x]
                cpu_count = int(cpu_item[0][1:]) if len(cpu_item) else gpu_count * n
                gpu_type = GPUType.A100
                gpu_memory = 80
                desc = f'Custom with {gpu_count}x {gpu_type.value}, {cpu_count} CPUs'
                instance_type = InstanceType(
                    name=instance_name,
                    cpu_count=cpu_count,
                    gpu_count=gpu_count,
                    gpu_type=gpu_type,
                    gpu_memory=gpu_memory,
                    desc=desc,
                )
                add_node_selector_to_instance(instance_type)
                return instance_type

            else:
                cpu_item = [x for x in items if 'c' in x]
                assert len(cpu_item), f'Unable to find number of cpus for instance: {instance_name}'
                cpu_count = int(cpu_item[0][1:])
                instance_type = InstanceType(
                    name=instance_name,
                    cpu_count=cpu_count,
                    gpu_count=gpu_count,
                    desc=f'Custom with {cpu_count} CPUs',
                )
                add_node_selector_to_instance(instance_type)
                return instance_type

        return None


R1Z1_INSTANCE_LIST = R1Z1InstanceList(instances=ALLOWED_INSTANCES)
