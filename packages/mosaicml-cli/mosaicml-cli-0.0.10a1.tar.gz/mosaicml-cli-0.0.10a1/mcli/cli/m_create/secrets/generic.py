"""Creators for generic secrets"""
from typing import Callable, Optional, Set

from mcli.cli.m_create.secrets.base import SecretCreator, SecretValidationError
from mcli.config import MCLIConfig
from mcli.config_objects.mcli_secret import (SECRET_MOUNT_PATH_PARENT, MCLIGenericEnvironmentSecret,
                                             MCLIGenericMountedSecret, MCLIGenericSecret, MCLIS3Secret, SecretType)
from mcli.utils.utils_interactive import get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_absolute_path, validate_secret_key


class GenericSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_value() -> str:
        return list_options('What data would you like to store?',
                            options=[],
                            helptext='',
                            pre_helptext=None,
                            allow_custom_response=True)


class GenericSecretValidator():
    """Validation methods for generic secret data
    """
    pass


class GenericSecretCreator(GenericSecretFiller, GenericSecretValidator):
    """Creates base generic secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               value: Optional[str] = None,
               do_import: Optional[bool] = None) -> MCLIGenericSecret:

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.generic, name=name, do_import=do_import)
        assert isinstance(secret, MCLIGenericSecret)

        if not secret.value:
            secret.value = value or self.fill_value()

        return secret


class GenericEnvSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_key(validate: Callable[[str], bool]) -> str:
        return list_options('If an environment variable is KEY=VALUE, what should be the KEY?',
                            options=[],
                            allow_custom_response=True,
                            pre_helptext=None,
                            validate=validate)


class GenericEnvSecretValidator():
    """Validation methods for env var secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_key_characters(key: str) -> bool:
        is_valid = validate_secret_key(key)
        if not is_valid:
            raise SecretValidationError(f'{FAIL} Invalid secret key. {is_valid.message}')
        return True

    @staticmethod
    def validate_key_available(key: str, existing_keys: Set[str]) -> bool:
        if key in existing_keys:
            raise SecretValidationError(f'{FAIL} Duplicate key. Environment variable key {key} already exists. '
                                        f'Please choose something not in {sorted(list(existing_keys))}.')
        return True

    @classmethod
    def validate_key(cls, key: str, existing_keys: Set[str]) -> bool:
        return cls.validate_key_characters(key) and cls.validate_key_available(key, existing_keys)


class GenericEnvSecretCreator(GenericEnvSecretFiller, GenericEnvSecretValidator):
    """Creates env var secrets for the CLI
    """

    @staticmethod
    def get_existing_keys() -> Set[str]:
        conf = MCLIConfig.load_config()
        env_keys = {ev.env_key for ev in conf.environment_variables}
        secret_keys = {s.env_key for s in conf.secrets if isinstance(s, MCLIGenericEnvironmentSecret) and s.env_key}
        return env_keys | secret_keys

    def create(self,
               name: Optional[str] = None,
               value: Optional[str] = None,
               key: Optional[str] = None,
               do_import: Optional[bool] = None) -> MCLIGenericEnvironmentSecret:

        # Validate key
        existing_keys = self.get_existing_keys()
        if key:
            self.validate_key(key, existing_keys)

        # Create generic secret
        generic_creator = GenericSecretCreator()
        generic_secret = generic_creator.create(name, value, do_import=do_import)

        # Fill key
        if not key:
            key = self.fill_key(get_validation_callback(self.validate_key, existing_keys))

        return MCLIGenericEnvironmentSecret.from_generic_secret(generic_secret, env_key=key)


class GenericFileSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_mount(default: str, validate: Callable[[str], bool]) -> str:
        return list_options('Where would you like the data to be mounted within your workload?',
                            options=[],
                            default_response=default,
                            allow_custom_response=True,
                            helptext=f'default: {default}',
                            pre_helptext=None,
                            validate=validate)


class GenericFileSecretValidator():
    """Validation methods for mounted secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    def __init__(self):
        self.existing_mounts = self.get_existing_mounts()

    @staticmethod
    def get_existing_mounts() -> Set[str]:
        conf = MCLIConfig.load_config()
        secret_paths = {s.mount_path for s in conf.secrets if isinstance(s, MCLIGenericMountedSecret) and s.mount_path}
        s3_mounts = {s.mount_directory for s in conf.secrets if isinstance(s, MCLIS3Secret) and s.mount_directory}
        return secret_paths | s3_mounts

    @staticmethod
    def validate_mount_absolute(path: str) -> bool:
        is_valid = validate_absolute_path(path)
        if not is_valid:
            raise SecretValidationError(f'{FAIL} Invalid mount point. Mount must be an absolute path, '
                                        f'not {path}.')
        return True

    @staticmethod
    def validate_mount_available(path: str, existing_paths: Set[str]) -> bool:
        if path in existing_paths:
            path_str = '\n'.join(sorted(list(existing_paths)))
            raise SecretValidationError(f'{FAIL} Duplicate path. Mount path {path} already in use.'
                                        f'Please choose something not in: {path_str}.')
        return True

    def validate_mount(self, path: str) -> bool:
        return self.validate_mount_absolute(path) and self.validate_mount_available(path, self.existing_mounts)


class GenericFileSecretCreator(GenericFileSecretFiller, GenericFileSecretValidator):
    """Creates mounted secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               value: Optional[str] = None,
               mount_path: Optional[str] = None,
               do_import: Optional[bool] = None) -> MCLIGenericMountedSecret:

        # Validate key
        if mount_path:
            self.validate_mount(mount_path)

        # Create generic secret
        generic_creator = GenericSecretCreator()
        generic_secret = generic_creator.create(name, value, do_import=do_import)

        # Fill key
        if not mount_path:
            mount_path = self.fill_mount(str(SECRET_MOUNT_PATH_PARENT / generic_secret.name),
                                         get_validation_callback(self.validate_mount))

        return MCLIGenericMountedSecret.from_generic_secret(generic_secret, mount_path=mount_path)
