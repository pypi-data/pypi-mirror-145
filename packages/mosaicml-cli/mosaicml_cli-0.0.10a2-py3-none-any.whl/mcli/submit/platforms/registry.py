""" A Singleton Platform Registry for all Sub Platforms """
from __future__ import annotations

import json
from typing import List, Optional

from mcli import config
from mcli.submit.platforms.aws import AWSPlatform
from mcli.submit.platforms.azure import AzurePlatform
from mcli.submit.platforms.cota import COTAPlatform
from mcli.submit.platforms.gcp import GCPPlatform
from mcli.submit.platforms.platform import Platform
from mcli.submit.platforms.r1z1 import R1Z1Platform
from mcli.submit.platforms.r6z1 import R6Z1Platform

platforms = {
    'aws': AWSPlatform,
    'azure': AzurePlatform,
    'gcp': GCPPlatform,
    'cota': COTAPlatform,
    'r1z1': R1Z1Platform,
    'r6z1': R6Z1Platform,
}

platform_context_names = {
    'aws': 'aws-research-01',
    'azure': 'azure-research-01',
    'gcp': 'gcp-research-01',
    'cota': 'colo-research-01',
    'r1z1': 'r1z1',
    'r6z1': 'r6z1',
}


class PlatformRegistry(object):
    """ A Singleton designed to track multiple platforms """

    def __init__(self):
        self._platforms = {}
        self._instance_lookup = {}

    def get(self, platform_name: str) -> Platform:
        """ Returns platform by name """
        if platform_name not in self._platforms:
            raise ValueError(f'No such platform: {platform_name}')
        else:
            return self._platforms[platform_name]

    def get_for_instance_type(self, instance_type: str) -> Platform:
        """ Returns platform by instance type """
        found_platform = None
        for platform in self._platforms.values():
            if platform.is_allowed_instance(instance_type):

                # check for duplicate allowed instances
                if found_platform is not None:
                    raise ValueError(f'{instance_type} found on multiple' + f'platforms: {found_platform}, {platform}.')
                else:
                    found_platform = platform

        if found_platform is None:
            raise ValueError(f'Instance type {instance_type} not in allowed instances.')
        else:
            return found_platform

    def register_platform(self, key: str, platform: Platform) -> None:
        """ add a created platform to the registry """
        if key in self._platforms:
            raise ValueError(f'Platform {key} already exists in registry.')
        else:
            self._platforms[key] = platform

    def available_platforms(self) -> List[str]:
        """ Returns all available platforms by name"""
        return list(self._platforms.keys())

    def __iter__(self):
        """ allow iteration through the platforms, returning (name, platform) tuples"""
        return iter(self._platforms.items())

    @classmethod
    def create_from_config(cls, mcli_config: dict) -> PlatformRegistry:
        """ creates a registry, and builds the platforms """
        register = PlatformRegistry()
        for key, platform_config in mcli_config.items():
            if key not in platforms:
                if key == 'r1z1':
                    continue
                raise ValueError(f'No such platform: {key}')
            else:
                platform = platforms[key](**platform_config)
                register.register_platform(key, platform)

        return register

    @classmethod
    def from_default_config(cls, config_path: Optional[str] = None) -> PlatformRegistry:
        path = config_path if config_path else config.MCTL_CONFIG_PATH
        with open(path, 'r', encoding='utf8') as f:
            config_data = json.load(f)

        return cls.create_from_config(mcli_config=config_data)
