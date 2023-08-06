""" The InstanceList of allowed COTA InstanceTypes """
import re
from typing import List, Optional, Set

from mcli.submit.platforms.instance_type import GPUType, InstanceList, InstanceType

DEFAULT_CPUS_PER_GPU = 15
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='cota-c1',
        cpu_count=1,
        gpu_count=0,
        desc='1 cpus',
    ),
    InstanceType(
        name='cota-c20',
        cpu_count=20,
        gpu_count=0,
        desc='20 cpus',
    ),
    InstanceType(
        name='cota-g1-3080',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='1x 3080s',
    ),
    InstanceType(
        name='cota-g2-3080',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='2x 3080s',
    ),
    InstanceType(
        name='cota-g4-3080',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='4x 3080s',
    ),
    InstanceType(
        name='cota-g8-3080',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='8x 3080s',
    ),
    InstanceType(
        name='cota-g1-3090',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='1x 3090s',
    ),
    InstanceType(
        name='cota-g2-3090',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='2x 3090s',
    ),
    InstanceType(
        name='cota-g4-3090',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='4x 3090s',
    ),
    InstanceType(
        name='cota-g8-3090',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='8x 3090s',
    ),
]

valid_cota_regex_configs = [
    r'cota-c[1-9]\d?\d?$',  # type: ignore
    'cota-g[1-8]$',
    'cota-g[1-8]-3080$',
    'cota-g[1-8]-3090$',
    r'cota-g[1-8]-c[1-9]\d?\d?-3080$',  # type: ignore
    r'cota-g[1-8]-c[1-9]\d?\d?-3090$',  # type: ignore
]


class CotaInstanceList(InstanceList):
    """ The Cota Instance List with Custom Naming Schema """

    def __init__(self, instances: List[InstanceType]) -> None:
        super().__init__(instances=instances)

    def get_allowed_instances(self) -> Set[str]:
        return {i.name for i in self.instances}

    def get_instance_by_name(self, instance_name: str) -> Optional[InstanceType]:
        for inst in self.instances:
            if inst.name == instance_name:
                return inst

        if any((re.match(x, instance_name) for x in valid_cota_regex_configs)):
            print(f'Matched: {instance_name}')
            items = instance_name.split('-')[1:]
            gpu_enabled = any(('g' in x for x in items))
            cpu_count = 0
            gpu_count = 0
            if gpu_enabled:
                gpu_count = int([x for x in items if 'g' in x][0][1:])
                cpu_item = [x for x in items if 'c' in x]
                cpu_count = int(cpu_item[0][1:]) if len(cpu_item) else gpu_count * n
                gpu_type = GPUType.RTX3080
                gpu_memory = 10
                if items[-1] == '3090':
                    gpu_type = GPUType.RTX3090
                    gpu_memory = 24
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


COTA_INSTANCE_LIST = CotaInstanceList(instances=ALLOWED_INSTANCES)

if __name__ == '__main__':
    print('hello')
    print(COTA_INSTANCE_LIST.get_instance_by_name(instance_name='cota-c15'))
    print(COTA_INSTANCE_LIST.get_instance_by_name(instance_name='cota-g6-3080'))
    print(COTA_INSTANCE_LIST.get_instance_by_name(instance_name='cota-g6-c21-3080'))
    print(COTA_INSTANCE_LIST.get_instance_by_name(instance_name='cota-g6-3090'))
    print(COTA_INSTANCE_LIST.get_instance_by_name(instance_name='cota-g6-c21-3090'))
