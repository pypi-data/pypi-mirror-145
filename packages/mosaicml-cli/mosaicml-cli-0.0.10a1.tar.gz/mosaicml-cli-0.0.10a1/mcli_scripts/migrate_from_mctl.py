"""Migrate MCTL config items to MCLI"""
import json
import re
import sys
import textwrap

from rich.progress import track
from yaspin.core import Yaspin

from mcli.config import MCTL_CONFIG_PATH, FeatureFlag, MCLIConfig, MCLIConfigError
from mcli.config_objects.mcli_secret import (MCLIDockerRegistrySecret, MCLIGenericEnvironmentSecret, MCLIPlatform,
                                             MCLISSHSecret, SecretType)
from mcli.utils.utils_kube import base64_decode, get_kube_contexts, list_secrets, read_secret

ok_prefix = '✅ '
fail_prefix = '💥 '


# pylint: disable=too-many-statements
def main() -> int:

    with Yaspin() as sp:
        sp.text = 'Migrating MCTL config...'
        sp.start()

        # Get current mcli config
        try:
            mcli_config = MCLIConfig.load_config()
            sp.write(f'{ok_prefix} Loaded current MCLI config')
        except MCLIConfigError:
            sp.write(f'{fail_prefix} No MCLI config file. First run `mcli init`')
            sp.stop()
            return 1

        # Fail if existing clusters are detected in mcli config
        if len(mcli_config.platforms) > 0:
            platform_names = [p.name for p in mcli_config.platforms]
            sp.write(f'{fail_prefix} Found existing platforms. To avoid incompatibilities, please delete these using '
                     f'`mcli delete platform {platform_names}`.')
            sp.stop()
            return 1
        assert len(mcli_config.platforms) == 0

        # Open mctl config
        if MCTL_CONFIG_PATH.exists():
            with open(MCTL_CONFIG_PATH, 'r', encoding='utf8') as fh:
                mctl_config = json.load(fh)
            sp.write(f'{ok_prefix} Loaded existing MCTL config')
        else:
            mctl_config = {}
            sp.write(f'{fail_prefix} No mctl config file found. Nothing to migrate.')
            sp.stop()
            return 1

        # Convert all mctl clusters to new platforms
        mctl_platforms = {}
        for cluster_name, cluster_info in mctl_config.items():
            # Create a platform for this cluster
            new_platform = MCLIPlatform(name=cluster_name,
                                        kubernetes_context=cluster_info['context_name'],
                                        namespace=cluster_info['namespace'])
            mctl_platforms[new_platform.name] = cluster_info
            mcli_config.platforms.append(new_platform)
        sp.write(f'{ok_prefix} Added existing mctl clusters to mcli')

        # Add any r*z* platforms in kube config
        platform_contexts = [p.kubernetes_context for p in mcli_config.platforms]
        kube_contexts = get_kube_contexts()

        def is_rz(x: str) -> bool:
            return re.match(r'r\dz\d', x, re.IGNORECASE) is not None

        unregistered_contexts = [x for x in kube_contexts if x.cluster not in platform_contexts and is_rz(x.cluster)]
        for new_context in unregistered_contexts:
            if new_context.namespace is not None:
                new_platform = MCLIPlatform(name=new_context.cluster,
                                            kubernetes_context=new_context.cluster,
                                            namespace=new_context.namespace)
                mcli_config.platforms.append(new_platform)
                sp.write(
                    f'{ok_prefix} Also found {new_context.cluster} context in your kube config and added it to mcli.')
            else:
                sp.write(f'{fail_prefix} Could not add kubernetes context {new_context.cluster} as a platform. '
                         'Please run `mcli create platform` and add it manually.')

        # Use cota and r1z1 as sources for these. Check r1z1 only if all are not found in cota
        source_platforms = []
        for name in ('colo-research-01', 'r1z1'):
            for platform in mcli_config.platforms:
                if platform.name == name:
                    source_platforms.append(platform)
                    break

        migrated = {key: False for key in ('docker', 'ssh', 'wandb')}
        new_secrets = []
        known_mcli_secrets = {x.name for x in mcli_config.secrets}
        for platform in source_platforms:
            if platform.name not in mctl_platforms:
                continue
            cluster_info = mctl_platforms[platform.name]
            with MCLIPlatform.use(platform):
                existing_secrets = {
                    secret['metadata']['name'] for secret in list_secrets(platform.namespace).get('items', [])
                }

                if not migrated['docker']:
                    # Check for docker secret and add it
                    # Get docker secret
                    docker_secret_name = cluster_info.get('image_pull_secrets', None)
                    if docker_secret_name in known_mcli_secrets:
                        sp.write(f'{ok_prefix} Docker registry secret already imported.')
                        migrated['docker'] = True
                    elif docker_secret_name and docker_secret_name in existing_secrets:
                        mcli_docker_secret = MCLIDockerRegistrySecret(name=docker_secret_name,
                                                                      secret_type=SecretType.docker_registry)
                        mcli_docker_secret.pull(platform)
                        new_secrets.append(mcli_docker_secret)
                        sp.write(f'{ok_prefix} Docker registry secret imported to mcli from cluster {platform.name}.')
                        migrated['docker'] = True

                if not migrated['ssh']:
                    # Check for ssh secret and convert it, then delete it
                    # Get ssh secret
                    ssh_secret_name = cluster_info.get('ssh_secrets', None)
                    new_name = f'{ssh_secret_name}-mcli'
                    if new_name in known_mcli_secrets:
                        sp.write(f'{ok_prefix} SSH secret already imported.')
                        migrated['ssh'] = True
                    elif ssh_secret_name and ssh_secret_name in existing_secrets:
                        mcli_ssh_secret = MCLISSHSecret(name=f'{ssh_secret_name}-mcli', secret_type=SecretType.ssh)
                        ssh_secret = read_secret(ssh_secret_name, platform.namespace)
                        assert ssh_secret and isinstance(ssh_secret['data'], dict)
                        mcli_ssh_secret.value = base64_decode(ssh_secret['data']['ssh_private_key'])
                        mcli_ssh_secret.mount_path = '/etc/secret/ssh/ssh-privatekey'
                        new_secrets.append(mcli_ssh_secret)
                        sp.write(f'{ok_prefix} SSH secret imported to mcli from cluster {platform.name}.')

                        # Disable DEPRECATED_SSH_KEY feature flag
                        if mcli_config.feature_enabled(FeatureFlag.DEPRECATED_SSH_KEY):
                            mcli_config.feature_flags[FeatureFlag.DEPRECATED_SSH_KEY.value] = False
                        migrated['ssh'] = True

                if not migrated['wandb']:
                    # Check for wandb secret and add it
                    wandb_secret_name = 'wandb'  # This wasn't specified in mctl config file
                    new_name = f'{wandb_secret_name}-mcli'
                    if new_name in known_mcli_secrets:
                        sp.write(f'{ok_prefix} WandB secret already imported.')
                        migrated['wandb'] = True
                    elif wandb_secret_name in existing_secrets:
                        mcli_wandb_secret = MCLIGenericEnvironmentSecret(name=f'{wandb_secret_name}-mcli',
                                                                         secret_type=SecretType.generic_environment)
                        wandb_secret = read_secret(wandb_secret_name, platform.namespace)
                        assert wandb_secret and isinstance(wandb_secret['data'], dict)
                        mcli_wandb_secret.value = base64_decode(wandb_secret['data']['wandb_api_key'])
                        mcli_wandb_secret.env_key = 'WANDB_API_KEY'
                        new_secrets.append(mcli_wandb_secret)
                        sp.write(f'{ok_prefix} WandB secret imported to mcli from cluster {platform.name}.')

                        # Disable DEPRECATED_WANDB_KEY feature flag
                        if mcli_config.feature_enabled(FeatureFlag.DEPRECATED_WANDB_KEY):
                            mcli_config.feature_flags[FeatureFlag.DEPRECATED_WANDB_KEY.value] = False
                            sp.write(f'{ok_prefix} Disabled DEPRECATED_WANDB_KEY feature flag.')
                        migrated['wandb'] = True

        not_migrated = [key for key, was_migrated in migrated.items() if was_migrated]
        if not not_migrated:
            sp.write(
                textwrap.dedent(f"""
                    Could not find a valid secret for the following types: {not_migrated}. You'll have to add them
                    manually using `mcli create secret`.
                    """))

        mcli_config.secrets.extend(new_secrets)
        with sp.hidden():
            for platform in track(mcli_config.platforms):
                for secret in new_secrets:
                    secret.sync_to_platform(platform)

        mcli_config.save_config()
        sp.write(f'{ok_prefix} Migration finished!')
        sp.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
