import copy
import json
import os
import tempfile

import pytest
import yaml

from mcli.submit.platforms.registry import PlatformRegistry


@pytest.fixture
def platform_registry() -> PlatformRegistry:
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Fake mosaic config
        config_path = tmpdirname + '/config'
        with open(config_path, 'w') as f:
            json.dump(
                {
                    'aws': {
                        'context_name': 'aws-research-01',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/aws',
                        'dataset_path': '/mnt/aws/datasets',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-test-user',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-aws-test-user'
                    },
                    'azure': {
                        'context_name': 'azure-research-01',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/azure',
                        'dataset_path': '/mnt/azure/datasets',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-niklas',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-azure-test-user'
                    },
                    'gcp': {
                        'context_name': 'gcp-research-01',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/gcp',
                        'dataset_path': '/mnt/gcp/datasets',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-test-user',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-gcp-test-user'
                    },
                    'cota': {
                        'context_name': 'colo-research-01',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/cota',
                        'dataset_path': '/localdisk',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-test-user',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-cota-test-user'
                    },
                    'r1z1': {
                        'context_name': 'r1z1',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/r1z1',
                        'dataset_path': '/mnt/r1z1/datasets',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-test-user',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-r1z1-test-user'
                    },
                    'r6z1': {
                        'context_name': 'r6z1',
                        'namespace': 'test-user',
                        'mount_path': '/mnt/r6z1',
                        'dataset_path': '/mnt/r6z1/datasets',
                        'image_pull_secrets': 'regcred',
                        'ssh_secrets': 'ssh-test-user',
                        'ssh_secrets_mount_path': '/etc/secret',
                        'pvc_name': 'pvc-r6z1-test-user'
                    }
                }, f)

        # Fake kubeconfig
        tmp_kubeconfig = tmpdirname + '/kubeconfig'
        os.environ['KUBECONFIG'] = tmp_kubeconfig
        with open(tmp_kubeconfig, 'w') as f:
            context = {
                'cluster': 'test-cluster',
                'namespace': 'test-user',
                'user': 'test-user',
            }

            yaml.dump(
                {
                    'apiVersion': 'v1',
                    'clusters': [{
                        'cluster': {
                            'server': 'https://foobar'
                        },
                        'name': 'test-cluster'
                    }],
                    'contexts': [{
                        'name': 'aws-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'azure-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'gcp-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'colo-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'r1z1',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'r6z1',
                        'context': copy.deepcopy(context),
                    }],
                    'current-context': 'aws-research-01'
                }, f)

        with open(os.environ['KUBECONFIG'], 'r') as f:
            print(f.read())

        return PlatformRegistry.from_default_config(config_path=config_path)
