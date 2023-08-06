""" Test Platform """
import pytest

from mcli.submit.platforms.platform import Platform
from mcli.submit.platforms.r1z1 import R1Z1_PRIORITY_CLASS_LABELS
from mcli.submit.platforms.registry import PlatformRegistry


def test_get_specs_gpu(platform_registry: PlatformRegistry):
    platform = platform_registry.get('aws')
    job_spec, _, _ = platform.get_specs('p4d.24xlarge')
    assert job_spec is not None
    assert job_spec.spec.template.spec.containers[0].resources['limits']['nvidia.com/gpu'] == 8
    assert job_spec.spec.template.spec.containers[0].resources['limits']['cpu'] == 96


def test_get_specs_ebs(platform_registry: PlatformRegistry):
    platform = platform_registry.get('aws')
    job_spec, otherspecs, _ = platform.get_specs('p4d.24xlarge', attach_ebs=True)
    assert job_spec is not None
    assert otherspecs is not None
    assert len(otherspecs) == 1
    assert otherspecs[0]['kind'] == 'PersistentVolumeClaim'
    name = otherspecs[0]['metadata']['name']
    ebs_volume = [
        volume for volume in job_spec.spec.template.spec.volumes if volume.persistent_volume_claim is not None
    ]
    assert len(ebs_volume) == 2
    assert ebs_volume[1].persistent_volume_claim.claim_name == name


def test_get_specs_ebs_non_compatible(platform_registry: PlatformRegistry):
    platform = platform_registry.get('gcp')
    job_spec, otherspecs, _ = platform.get_specs('n1-standard-32', attach_ebs=True)
    assert job_spec is not None
    assert otherspecs is not None
    assert len(otherspecs) == 0


def get_first_instance(platform: Platform) -> str:
    instances = platform.allowed_instances.get_allowed_instances()
    return list(instances)[0]


@pytest.mark.parametrize('priority_name', ('scavenge', 'standard', 'emergency'))
@pytest.mark.parametrize('platform_name', ('r1z1', 'r6z1'))
def test_get_specs_priority(platform_name: str, priority_name: str, platform_registry: PlatformRegistry):
    """Test that r1z1 platform priorities get set properly within the resulting job spec

    Args:
        platform_name (str): Platform name
        priority_name (str): Priority class name
        platform_registry (PlatformRegistry): Custom platform registry
    """
    platform = platform_registry.get(platform_name)
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance, priority_class=priority_name)
    assert job_spec is not None
    selected_priority = job_spec.spec.template.spec.priority_class_name
    assert selected_priority == R1Z1_PRIORITY_CLASS_LABELS[priority_name]


@pytest.mark.parametrize('platform_name', ('r1z1', 'r6z1'))
def test_get_specs_priority_default(platform_name: str, platform_registry: PlatformRegistry):
    """Test that r1z1 platform priorities properly handle a priority of None as default

    Args:
        platform_name (str): Platform name
        platform_registry (PlatformRegistry): Custom platform registry
    """

    platform = platform_registry.get(platform_name)
    assert platform.default_priority_class is not None
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance, priority_class=None)
    assert job_spec is not None
    selected_priority = job_spec.spec.template.spec.priority_class_name
    assert selected_priority == R1Z1_PRIORITY_CLASS_LABELS[platform.default_priority_class]


@pytest.mark.parametrize('platform_name', ('aws', 'gcp'))
def test_get_specs_priority_none(platform_name: str, platform_registry: PlatformRegistry):
    """Test that a few platforms priorities properly handle a priority of None

    Args:
        platform_name (str): Name of the platform
        platform_registry (PlatformRegistry): Custom platform registry
    """

    platform = platform_registry.get(platform_name)
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance, priority_class=None)
    assert job_spec is not None
    selected_priority = job_spec.spec.template.spec.priority_class_name
    assert selected_priority is None


@pytest.mark.parametrize('platform_name', ('aws', 'r1z1', 'r6z1', 'gcp'))
def test_get_specs_priority_invalid(platform_name: str, platform_registry: PlatformRegistry):
    """Test that a few platforms priorities properly handle an incorrect priority name

    Args:
        platform_name (str): Name of the platform
        platform_registry (PlatformRegistry): Custom platform registry
    """

    platform = platform_registry.get(platform_name)
    instance = get_first_instance(platform)
    with pytest.raises(ValueError):
        _, _, _ = platform.get_specs(instance, priority_class='not-a-real-class')


def test_ssh_secrets():
    """Test that SSH secrets are properly mounted
    """
    platform_config = {
        'r1z1': {
            'context_name': 'r1z1',
            'namespace': 'test-user',
            'mount_path': '/mnt/r1z1',
            'dataset_path': '/mnt/r1z1/datasets',
            'image_pull_secrets': 'regcred',
            'pvc_name': 'pvc-r1z1-test-user',
            'ssh_secrets': 'secrets-foo',
            'ssh_secrets_mount_path': '/mnt/ssh_secret'
        }
    }
    platform = PlatformRegistry.create_from_config(platform_config).get('r1z1')
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance)

    # Assert ssh volume mount
    mounts = job_spec.spec.template.spec.containers[0].volume_mounts
    mounts = [vm for vm in mounts if vm.name == 'secret-ssh-volume']
    assert len(mounts) > 0
    mount = mounts[0]
    assert mount.mount_path == platform_config['r1z1']['ssh_secrets_mount_path']

    # Assert ssh volume
    volumes = job_spec.spec.template.spec.volumes
    volumes = [v for v in volumes if v.name == 'secret-ssh-volume']
    assert len(volumes) > 0
    volume = volumes[0]
    assert volume.secret.secret_name == platform_config['r1z1']['ssh_secrets']

    # Assert GIT_SSH_COMMAND env var
    envs = job_spec.spec.template.spec.containers[0].env
    assert any(ev.name == 'GIT_SSH_COMMAND' for ev in envs)


def test_no_ssh_secrets():
    """Test that SSH secrets are not mounted when not requested
    """
    platform_config = {
        'r1z1': {
            'context_name': 'r1z1',
            'namespace': 'test-user',
            'mount_path': '/mnt/r1z1',
            'dataset_path': '/mnt/r1z1/datasets',
            'image_pull_secrets': 'regcred',
            'pvc_name': 'pvc-r1z1-test-user'
        }
    }
    platform = PlatformRegistry.create_from_config(platform_config).get('r1z1')
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance)
    # No ssh volume mount
    mounts = job_spec.spec.template.spec.containers[0].volume_mounts
    assert not any(vm.name == 'secret-ssh-volume' for vm in mounts)

    # No ssh volume
    volumes = job_spec.spec.template.spec.volumes
    assert not any(v.name == 'secret-ssh-volume' for v in volumes)

    # No GIT_SSH_COMMAND env var
    envs = job_spec.spec.template.spec.containers[0].env
    assert not any(ev.name == 'GIT_SSH_COMMAND' for ev in envs)


def test_image_pull_secrets():
    """Test that image pull secrets are properly added
    """
    platform_config = {
        'r1z1': {
            'context_name': 'r1z1',
            'namespace': 'test-user',
            'mount_path': '/mnt/r1z1',
            'dataset_path': '/mnt/r1z1/datasets',
            'image_pull_secrets': 'image-secret',
            'pvc_name': 'pvc-r1z1-test-user',
        }
    }
    platform = PlatformRegistry.create_from_config(platform_config).get('r1z1')
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance)

    # Assert image_pull_secret
    pod_spec = job_spec.spec.template.spec
    assert len(pod_spec.image_pull_secrets) > 0
    assert pod_spec.image_pull_secrets[0].name == platform_config['r1z1']['image_pull_secrets']


def test_no_image_pull_secrets():
    """Test that no image pull secret is added if not requested
    """
    platform_config = {
        'r1z1': {
            'context_name': 'r1z1',
            'namespace': 'test-user',
            'mount_path': '/mnt/r1z1',
            'dataset_path': '/mnt/r1z1/datasets',
            'pvc_name': 'pvc-r1z1-test-user',
        }
    }
    platform = PlatformRegistry.create_from_config(platform_config).get('r1z1')
    instance = get_first_instance(platform)
    job_spec, _, _ = platform.get_specs(instance)

    # Assert image_pull_secret
    pod_spec = job_spec.spec.template.spec
    assert pod_spec.image_pull_secrets is None
