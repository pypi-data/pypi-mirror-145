""" Used for getting information on Platforms """

from typing import List

from mcli.config import get_mcli_config
from mcli.config_objects import MCLIPlatform


def get_platform_list() -> List[MCLIPlatform]:
    conf = get_mcli_config()
    return conf.platforms
