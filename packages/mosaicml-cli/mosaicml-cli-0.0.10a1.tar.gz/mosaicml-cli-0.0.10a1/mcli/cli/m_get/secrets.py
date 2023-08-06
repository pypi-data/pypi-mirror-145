"""CLI getter for secrets"""
from dataclasses import dataclass
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.config_objects.mcli_secret import MCLISecret, SecretType
from mcli.utils.utils_logging import FAIL, err_console


@dataclass
class SecretDisplayItem(MCLIDisplayItem):
    name: str
    type: SecretType


class MCLISecretDisplay(MCLIGetDisplay):
    """`mcli get secrets` display class
    """

    def __init__(self, secrets: List[MCLISecret]):
        self.secrets = secrets

    def __iter__(self) -> Generator[SecretDisplayItem, None, None]:
        for secret in self.secrets:
            yield SecretDisplayItem(name=secret.name, type=secret.secret_type)


def get_secrets(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        conf: MCLIConfig = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. Please run `mcli init` and then `mcli create secret` '
                          'to create your first secret.')
        return 1

    display = MCLISecretDisplay(conf.secrets)
    display.print(output)
    return 0
