""" The MCLI Abstraction for Environment Variables """
from dataclasses import dataclass

from mcli.utils.utils_serializable_dataclass import SerializableDataclass


@dataclass
class MCLIEnvVar(SerializableDataclass):
    # TODO(averylamp): This is a WIP to be flushed out more later
    name: str
    env_key: str
    env_value: str
