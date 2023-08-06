"""Base creator for secrets"""
import logging
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Set

from mcli.config import MCLIConfig
from mcli.config_objects.mcli_platform import MCLIPlatform
from mcli.config_objects.mcli_secret import SECRET_CLASS_MAP, MCLISecret, SecretType
from mcli.utils.utils_interactive import ValidationError, get_validation_callback, list_options, query_yes_no
from mcli.utils.utils_kube import list_secrets
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, console
from mcli.utils.utils_string_validation import validate_secret_name

logger = logging.getLogger(__name__)


class ExistingSecret(NamedTuple):
    name: str
    is_mcli: bool


class SecretValidationError(ValidationError):
    """Secret could not be configured with the provided values
    """


class SecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_name(validate: Callable[[str], bool]) -> str:
        return list_options(
            input_text='What would you like to name this secret?',
            options=[],
            helptext='Must be unique',
            pre_helptext=None,
            allow_custom_response=True,
            validate=validate,
        )


class SecretValidator():
    """Validation methods for secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_one_platform_exists(platforms: List[MCLIPlatform]) -> bool:

        if not platforms:
            raise SecretValidationError(
                f'{FAIL} No platforms found. You must have at least one platform setup before you add secrets. '
                'Please try running `mcli create platform` first to generate one.')
        return True

    @staticmethod
    def validate_secret_name_available(name: str, existing_names: Set[str]) -> bool:

        if name in existing_names:
            raise SecretValidationError(f'{FAIL} Existing secret. Secret named {name} already exists. Please choose '
                                        f'something not in {sorted(list(existing_names))}.')
        return True

    @staticmethod
    def validate_secret_name_rfc(name: str) -> bool:

        result = validate_secret_name(name)
        if not result:
            raise SecretValidationError(f'{FAIL} {result.message}')
        return True

    @classmethod
    def validate_secret_name_full(cls, name: str, existing_names: Set[str]) -> bool:
        return cls.validate_secret_name_rfc(name) and cls.validate_secret_name_available(name, existing_names)

    @staticmethod
    def validate_kube_secret_name(name: str, existing_kube_secrets: List[ExistingSecret],
                                  poss_import: Optional[bool]) -> bool:
        existing_secret_map = {s.name: s.is_mcli for s in existing_kube_secrets}
        if name in existing_secret_map:
            if poss_import is False:
                raise SecretValidationError(f'{FAIL} A secret named {name} already exists.'
                                            f' Please choose a name not in {sorted(list(existing_secret_map.keys()))}.')
            is_mcli = existing_secret_map[name]
            if not is_mcli:
                raise SecretValidationError(
                    f'{FAIL} A secret named {name} already exists but is not an `mcli` created secret.'
                    f' Please choose a name not in {sorted(list(existing_secret_map.keys()))}.')
            return False
        return True


class SecretCreator(SecretValidator, SecretFiller):
    """Creates base secrets for the CLI
    """

    @staticmethod
    def get_existing_platform_secrets(platform: MCLIPlatform) -> List[ExistingSecret]:
        is_mcli = lambda secret: label.mosaic.MCLI_VERSION in secret['metadata'].get('labels', {})
        with MCLIPlatform.use(platform):
            secret_list: List[Dict[str, Any]] = list_secrets(platform.namespace)['items']
            existing_secrets = [ExistingSecret(secret['metadata']['name'], is_mcli(secret)) for secret in secret_list]
        return existing_secrets

    @staticmethod
    def create_base_secret(name: str, secret_type: SecretType) -> MCLISecret:
        secret_class = SECRET_CLASS_MAP.get(secret_type)
        if not secret_class:
            raise SecretValidationError(f'{FAIL} The secret type: {secret_type} does not exist.')

        return secret_class(name, secret_type)

    def create(self,
               secret_type: SecretType,
               name: Optional[str] = None,
               do_import: Optional[bool] = None,
               **kwargs) -> MCLISecret:

        del kwargs

        conf = MCLIConfig.load_config()
        self.validate_one_platform_exists(conf.platforms)
        ref_platform = conf.platforms[0]

        existing_secret_names = {secret.name for secret in conf.secrets}
        if name:
            self.validate_secret_name_full(name, existing_secret_names)

        if not name:
            name = self.fill_name(
                validate=get_validation_callback(self.validate_secret_name_full, existing_secret_names))

        base_secret = self.create_base_secret(name, secret_type)

        existing_kube_secrets = self.get_existing_platform_secrets(ref_platform)
        valid_k8s_secret = self.validate_kube_secret_name(name, existing_kube_secrets, do_import)

        if not valid_k8s_secret:
            logger.info(f'A secret with name {name} already exists in platform {ref_platform.name}.')
            if do_import is None:
                do_import = query_yes_no(
                    f'Would you like to try to import the secret from platform {ref_platform.name}?')
            if not do_import:
                existing_kube_names = sorted([s.name for s in existing_kube_secrets])
                raise SecretValidationError(f'{FAIL} A secret named {name} already exists.'
                                            f' Please choose a name not in {existing_kube_names}.')
            with console.status(f'Importing from {ref_platform.name}'):
                base_secret.pull(ref_platform)

        return base_secret
