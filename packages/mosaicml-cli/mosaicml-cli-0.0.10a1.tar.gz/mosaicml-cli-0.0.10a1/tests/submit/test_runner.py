from mcli.submit.kubernetes.mcli_job import MCLIJob
from mcli.submit.kubernetes.runners import Runner
from mcli.submit.platforms.registry import PlatformRegistry


def test_runner(platform_registry: PlatformRegistry):
    runner = Runner(platform_registry=platform_registry)
    job = MCLIJob(name='foobar', container_image='test-container')
    empty_cm, job_spec = runner.get_specs(job, 'c5.large')

    env = job_spec['spec']['template']['spec']['containers'][0]['env']
    instance_variable = [kv for kv in env if kv['name'] == 'MOSAICML_INSTANCE_TYPE']
    assert len(instance_variable) == 1
    assert instance_variable[0]['value'] == 'c5.large'
    assert job_spec['spec']['template']['spec']['containers'][0]['image'] == 'test-container'

    assert job_spec['metadata']['labels']['mosaicml.com/job'] == 'foobar'
    assert empty_cm['metadata']['labels']['mosaicml.com/job'] == 'foobar'
    assert job_spec['spec']['template']['metadata']['labels']['mosaicml.com/job'] == 'foobar'
    assert job_spec['metadata']['labels']['mosaicml.com/instance'] == 'c5.large'
    assert empty_cm['metadata']['labels']['mosaicml.com/instance'] == 'c5.large'
    assert job_spec['spec']['template']['metadata']['labels']['mosaicml.com/instance'] == 'c5.large'
