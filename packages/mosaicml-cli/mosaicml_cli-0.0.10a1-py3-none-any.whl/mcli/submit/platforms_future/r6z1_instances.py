""" Available Instances for the R6Z1 Platform """
import re
from typing import List, Optional, Set

from mcli.submit.platforms_future.experimental import ExperimentalFlag
from mcli.submit.platforms_future.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 7
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='r6z1-g1-a100',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='1x a100s',
    ),
    InstanceType(
        name='r6z1-g2-a100',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='2x a100s',
    ),
    InstanceType(
        name='r6z1-g4-a100',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='4x a100s',
    ),
    InstanceType(
        name='r6z1-g8-a100',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='8x a100s',
    ),
]


def add_node_selector_to_instance(instance: InstanceType) -> None:
    instance.extras.update({'node_selector': label.mosaic.NODE_CLASS})

    if instance.gpu_type == GPUType.A100:
        instance.extras.update({'node_class': 'a100-40sxm'})


def add_experimental_flags_to_instance(instance: InstanceType) -> None:
    """Adds available experimental flags to each applicable instance

    Args:
        instance (InstanceType): Instance to add flags to
    """
    if instance.gpu_count == 8:
        instance.extras.setdefault('experimental', []).append(ExperimentalFlag.RDMA)


for r6z1_instance in ALLOWED_INSTANCES:
    add_node_selector_to_instance(r6z1_instance)
    add_experimental_flags_to_instance(r6z1_instance)

valid_r6z1_regex_configs = [
    'r6z1-g[1-8]-a100$',
    r'r6z1-g[1-8]-c[1-9]\d?\d?-a100',  # type: ignore
]


class R6Z1InstanceList(InstanceList):
    """ Available Instances for the R6Z1 Platform """

    def __init__(self, instances: List[InstanceType]) -> None:
        super().__init__(instances=instances)

    def get_allowed_instances(self) -> Set[str]:
        return {i.name for i in self.instances}

    def get_instance_by_name(self, instance_name: str) -> Optional[InstanceType]:
        for inst in self.instances:
            if inst.name == instance_name:
                return inst

        if any((re.match(x, instance_name) for x in valid_r6z1_regex_configs)):
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
                gpu_memory = 40
                desc = f'Custom with {gpu_count}x {gpu_type.value}, {cpu_count} CPUs'
                return InstanceType(
                    name=instance_name,
                    cpu_count=cpu_count,
                    gpu_count=gpu_count,
                    gpu_type=gpu_type,
                    gpu_memory=gpu_memory,
                    desc=desc,
                )

            else:
                cpu_item = [x for x in items if 'c' in x]
                assert len(cpu_item), f'Unable to find number of cpus for instance: {instance_name}'
                cpu_count = int(cpu_item[0][1:])
                return InstanceType(
                    name=instance_name,
                    cpu_count=cpu_count,
                    gpu_count=gpu_count,
                    desc=f'Custom with {cpu_count} CPUs',
                )

        return None


R6Z1_INSTANCE_LIST = R6Z1InstanceList(instances=ALLOWED_INSTANCES)
