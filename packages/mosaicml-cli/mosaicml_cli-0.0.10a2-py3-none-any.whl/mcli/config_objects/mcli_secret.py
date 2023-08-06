""" MCLI Abstraction for Secrets """
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, Union

import yaml
from kubernetes import client

from mcli import version
from mcli.config_objects.mcli_platform import MCLIPlatform
from mcli.submit.kubernetes.mcli_job_future import MCLIK8sJob, MCLIVolume
from mcli.utils.utils_kube import base64_decode, base64_encode, create_secret, read_secret, update_secret
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_serializable_dataclass import SerializableDataclass, T_SerializableDataclass

SECRET_MOUNT_PATH_PARENT = Path('/etc/secret')


class SecretType(Enum):
    """ Enum for Types of Secrets Allowed """
    docker_registry = 'docker_registry'
    ssh = 'ssh'
    generic = 'generic'
    generic_mounted = 'generic_mounted'
    generic_environment = 'generic_environment'
    s3_credentials = 's3_credentials'

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def ensure_enum(cls, val: Union[str, SecretType]) -> SecretType:
        if isinstance(val, str):
            return SecretType[val]
        elif isinstance(val, SecretType):
            return val
        raise ValueError(f'Unable to ensure {val} is a SecretType Enum')


@dataclass
class MCLISecret(SerializableDataclass, ABC):
    """
    The Base Secret Class for MCLI Secrets

    Secrets can not nest other SerializableDataclass objects
    """

    name: str
    secret_type: SecretType

    @property
    def kubernetes_type(self) -> str:
        """The corresponding Kubernetes secret type for this class of secrets
        """
        return 'Opaque'

    @abstractmethod
    def add_to_job(self, mcli_job: MCLIK8sJob) -> bool:
        """Add a secret to a job
        """

    @property
    def required_packing_fields(self) -> Set[str]:
        """ All required fields for packing up the secret
        """
        return set()

    def unpack(self, data: Dict[str, str]):
        """Unpack the Kubernetes secret `data` field to fill in required secret values

        All required packing fields must be present.
        By default looks for all required fields and base64 decodes them

        Args:
            data (Dict[str, str]): _description_
        """

        missing_fields = self.required_packing_fields - data.keys()
        if missing_fields:
            raise ValueError('Missing required field(s) to unpack Secret: '
                             f'{",".join(missing_fields)}')

        for required_field in self.required_packing_fields:
            setattr(self, required_field, base64_decode(data[required_field]))

    def pack(self) -> Dict[str, str]:
        """The `data` field for the corresponding kubernetes secret
        Validated to ensure fully completed

        By default base64 encodes all required fields
        """
        filled_fields = asdict(self)
        data = {k: v for k, v in filled_fields.items() if k in self.required_packing_fields}
        for key, value in data.items():
            if not isinstance(value, str):
                raise TypeError(f'All keys in a secret must be strings, got {key}: {type(value)}')
            data[key] = base64_encode(value)
        return data

    def pull(self, platform: MCLIPlatform):
        with MCLIPlatform.use(platform):
            # Read the secret if it exists
            secret = read_secret(self.name, platform.namespace)
            if not secret:
                raise RuntimeError(f'Could not find secret {self.name} in platform {platform.name}')
            assert isinstance(secret['data'], dict)
            self.unpack(secret['data'])

    @classmethod
    def from_dict(cls: Type[T_SerializableDataclass], data: Dict[str, Any]) -> T_SerializableDataclass:
        secret_type = data.get('secret_type', None)
        if not secret_type:
            raise ValueError(f'No `secret_type` found for secret with data: \n{yaml.dump(data)}')

        secret_type: SecretType = SecretType.ensure_enum(secret_type)
        data['secret_type'] = secret_type

        secret: Optional[MCLISecret] = None
        if secret_type == SecretType.docker_registry:
            secret = MCLIDockerRegistrySecret(**data)
        elif secret_type == SecretType.generic_mounted:
            secret = MCLIGenericMountedSecret(**data)
        elif secret_type == SecretType.generic_environment:
            secret = MCLIGenericEnvironmentSecret(**data)
        elif secret_type == SecretType.ssh:
            secret = MCLISSHSecret(**data)
        elif secret_type == SecretType.s3_credentials:
            secret = MCLIS3Secret(**data)
        else:
            raise NotImplementedError(f'Secret of type: { secret_type } not supported yet')
        assert isinstance(secret, MCLISecret)
        return secret  # type: ignore

    @property
    def kubernetes_labels(self) -> Dict[str, str]:
        """Labels to add to all Kubernetes secrets
        """
        labels = {
            label.mosaic.SECRET_TYPE: self.secret_type.value.replace('_', '-'),
            label.mosaic.MCLI_VERSION: str(version.__version__),
            label.mosaic.MCLI_VERSION_MAJOR: str(version.__version_major__),
            label.mosaic.MCLI_VERSION_MINOR: str(version.__version_minor__),
            label.mosaic.MCLI_VERSION_PATCH: str(version.__version_patch__),
        }
        return labels

    @property
    def kubernetes_annotations(self) -> Dict[str, str]:
        """Annotations to add to all Kubernetes secrets
        """
        return {}

    def sync_to_platform(self, platform: MCLIPlatform) -> bool:
        """Sync a secret to the given platform

        Args:
            platform: Platform to sync secret with

        Returns:
            bool: True if sync was successful
        """
        with MCLIPlatform.use(platform):
            # Check if secret exists in current context
            secret = read_secret(self.name, platform.namespace)

            success: bool
            data = self.pack()
            if secret is not None:  # secret exists
                # Patch existing secret
                success = update_secret(
                    self.name,
                    platform.namespace,
                    data,
                    labels=self.kubernetes_labels,
                    annotations=self.kubernetes_annotations,
                )
            else:
                # Create secret
                success = create_secret(
                    self.name,
                    platform.namespace,
                    data,
                    self.kubernetes_type,
                    labels=self.kubernetes_labels,
                    annotations=self.kubernetes_annotations,
                )

        return success


@dataclass
class MCLIDockerRegistrySecret(MCLISecret):
    """Secret class for docker image pull secrets
    """
    docker_username: Optional[str] = None
    docker_password: Optional[str] = None
    docker_email: Optional[str] = None
    docker_server: Optional[str] = None

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['docker_username', 'docker_password', 'docker_email', 'docker_server']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields)

    @property
    def kubernetes_type(self) -> str:
        """The corresponding Kubernetes secret type for this class of secrets
        """
        return 'kubernetes.io/dockerconfigjson'

    def unpack(self, data: Dict[str, str]):
        """Unpack the Kubernetes secret `data` field to fill in required secret values

        Args:
            data: _description_
        """

        if '.dockerconfigjson' in data:
            values: Dict[str, Any] = json.loads(base64_decode(data['.dockerconfigjson']))
            values = values['auths']
            missing = set()

            docker_servers = values.keys()
            if len(docker_servers) != 1:
                raise KeyError(f'{len(docker_servers)} Docker Servers detected.'
                               ' Must have only one specified')
            self.docker_server = list(docker_servers)[0]
            values = values[self.docker_server]

            for required in ('username', 'password', 'email'):
                if required not in values:
                    missing.add(required)
            if missing:
                raise KeyError(f'Incompatible secret: Docker secret is missing the following keys: {missing}')

            self.docker_username = values['username']
            self.docker_password = values['password']
            self.docker_email = values['email']
        else:
            raise KeyError('Docker secret must have the key ".dockerconfigjson"')

    def pack(self) -> Dict[str, str]:
        filled_fields = asdict(self)
        missing_fields = self.required_packing_fields - filled_fields.keys()
        if missing_fields:
            raise ValueError('Missing required field(s) to unpack Secret: '
                             f'{",".join(missing_fields)}')

        data = {
            'auths': {
                self.docker_server: {
                    'username': self.docker_username,
                    'password': self.docker_password,
                    'email': self.docker_email,
                    'auth': base64_encode(f'{self.docker_username}:{self.docker_password}'),
                }
            }
        }
        json_str = json.dumps(data)
        return {'.dockerconfigjson': base64_encode(json_str)}

    def add_to_job(self, mcli_job: MCLIK8sJob) -> bool:
        if mcli_job.pod_spec.image_pull_secrets and isinstance(mcli_job.pod_spec.image_pull_secrets, list):
            mcli_job.pod_spec.image_pull_secrets.append(client.V1LocalObjectReference(name=self.name))
        else:
            mcli_job.pod_spec.image_pull_secrets = [client.V1LocalObjectReference(name=self.name)]
        return True


@dataclass
class MCLIGenericSecret(MCLISecret):
    """Secret class for generic secrets
    """
    value: Optional[str] = None

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['value']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields)

    def unpack(self, data: Dict[str, str]):
        """Unpack the Kubernetes secret `data` field to fill in required secret values

        Args:
            data (Dict[str, str]): _description_
        """

        if 'value' not in data:
            raise KeyError('Incompatible secret: Secret is missing the "value" key.')
        self.value = base64_decode(data['value'])

    def add_to_job(self, mcli_job: MCLIK8sJob) -> bool:
        del mcli_job
        # Missing context on how it should be added to a job
        raise NotImplementedError


@dataclass
class MCLIGenericMountedSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be mounted to run pods as files
    """
    mount_path: Optional[str] = None

    @property
    def required_packing_fields(self) -> Set[str]:
        # Note: mount_path is written to k8s but also disk to allow for add_to_job
        # without syncing secrets
        return set(self.disk_skipped_fields + ['mount_path'])

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIGenericMountedSecret],
        generic_secret: MCLIGenericSecret,
        mount_path: str,
    ) -> MCLIGenericMountedSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.generic_mounted,
            mount_path=mount_path,
        )

    def add_to_job(self, mcli_job: MCLIK8sJob, permissions: int = 420) -> bool:
        assert self.mount_path is not None
        path = Path(self.mount_path)
        secret_volume = client.V1Volume(
            name=self.name,
            secret=client.V1SecretVolumeSource(
                secret_name=self.name,
                items=[client.V1KeyToPath(key='value', path=path.name)],
                default_mode=permissions,
            ),
        )
        secret_mount = client.V1VolumeMount(
            name=self.name,
            mount_path=str(path.parent),
            read_only=True,
        )
        mcli_volume = MCLIVolume(volume=secret_volume, volume_mount=secret_mount)
        mcli_job.add_volume(mcli_volume)
        return True


@dataclass
class MCLIGenericEnvironmentSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be added as environment variables
    """
    env_key: Optional[str] = None

    @property
    def required_packing_fields(self) -> Set[str]:
        # Note: env_key is written to k8s but also disk to allow for add_to_job
        # without syncing secrets
        return set(self.disk_skipped_fields + ['env_key'])

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIGenericEnvironmentSecret],
        generic_secret: MCLIGenericSecret,
        env_key: str,
    ) -> MCLIGenericEnvironmentSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.generic_environment,
            env_key=env_key,
        )

    def add_to_job(self, mcli_job: MCLIK8sJob) -> bool:
        secret_env = client.V1EnvVar(
            name=self.env_key,
            value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(
                name=self.name,
                key='value',
                optional=False,
            ),),
        )

        mcli_job.add_environment_variable(secret_env)
        return True


@dataclass
class MCLISSHSecret(MCLIGenericMountedSecret):
    """Secret class for ssh private keys that will be mounted to run pods as a file

    Overrides Git SSH Command to use the SSH key
    """
    ssh_private_key: Optional[str] = None

    def __post_init__(self):
        if self.ssh_private_key and not self.value:
            with open(self.ssh_private_key, 'r', encoding='utf8') as fh:
                self.value = fh.read()

    def unpack(self, data: Dict[str, str]):
        if 'ssh-privatekey' in data:
            data.setdefault('value', data['ssh-privatekey'])
        return super().unpack(data)

    def pack(self) -> Dict[str, str]:
        packed = super().pack()
        if self.ssh_private_key:
            packed['ssh-privatekey'] = packed['value']
        return packed

    def add_to_job(self, mcli_job: MCLIK8sJob, permissions: int = 256) -> bool:
        super().add_to_job(mcli_job=mcli_job, permissions=permissions)
        git_ssh_command_var = client.V1EnvVar(
            name='GIT_SSH_COMMAND',
            value=f'ssh -i {self.mount_path}',
        )
        mcli_job.add_environment_variable(git_ssh_command_var)
        return True


@dataclass
class MCLIS3Secret(MCLISecret):
    """Secret class for AWS credentials
    """
    mount_directory: Optional[str] = None
    credentials: Optional[str] = None
    config: Optional[str] = None

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['credentials', 'config']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields + ['mount_directory'])

    def add_to_job(self, mcli_job: MCLIK8sJob) -> bool:
        assert self.mount_directory is not None
        path = Path(self.mount_directory)
        secret_volume = client.V1Volume(
            name=self.name,
            secret=client.V1SecretVolumeSource(
                secret_name=self.name,
                items=[
                    client.V1KeyToPath(key='credentials', path='credentials'),
                    client.V1KeyToPath(key='config', path='config'),
                ],
            ),
        )
        secret_mount = client.V1VolumeMount(
            name=self.name,
            mount_path=str(path),
            read_only=True,
        )
        mcli_volume = MCLIVolume(volume=secret_volume, volume_mount=secret_mount)
        mcli_job.add_volume(mcli_volume)

        # Add config and credential env vars
        config_var = client.V1EnvVar(
            name='AWS_CONFIG_FILE',
            value=f'{self.mount_directory}/config',
        )
        mcli_job.add_environment_variable(config_var)
        cred_var = client.V1EnvVar(
            name='AWS_SHARED_CREDENTIALS_FILE',
            value=f'{self.mount_directory}/credentials',
        )
        mcli_job.add_environment_variable(cred_var)
        return True


SECRET_CLASS_MAP: Dict[SecretType, Type[MCLISecret]] = {
    SecretType.docker_registry: MCLIDockerRegistrySecret,
    SecretType.generic: MCLIGenericSecret,
    SecretType.generic_environment: MCLIGenericEnvironmentSecret,
    SecretType.generic_mounted: MCLIGenericMountedSecret,
    SecretType.ssh: MCLISSHSecret,
    SecretType.s3_credentials: MCLIS3Secret,
}
