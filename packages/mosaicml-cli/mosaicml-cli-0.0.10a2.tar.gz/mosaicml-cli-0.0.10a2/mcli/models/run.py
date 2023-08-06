""" Run Model """
from __future__ import annotations

import logging
import uuid
import warnings
from dataclasses import asdict, dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union

from mcli.utils.utils_yaml import load_yaml

log = logging.getLogger(__name__)


class RunStatus(Enum):
    SUBMITTED = 'submitted'
    # TODO: add other run types


@dataclass
class RunModel:
    """ Run Model """

    run_id: str
    name: str
    instance: str
    image: str
    git_repo: str
    git_branch: str

    # Generated unless otherwise provided
    command: str
    parameters: Dict[str, Any]

    @classmethod
    def from_partial_run_model(cls, partial_run_model: PartialRunModel) -> RunModel:
        """Create a RunModel from the provided PartialRunModel.

        If the PartialRunModel is not fully populated then this function fails with an error.

        Args:
            partial_run_model (PartialRunModel): The PartialRunModel

        Returns:
            RunModel: The RunModel object created using values from the PartialRunModel
        """

        model_as_dict = asdict(partial_run_model)
        missing_fields = [field for field, value in model_as_dict.items() if value is None]
        if len(missing_fields) > 0:
            log.error(f'[ERROR] Cannot construct run because of missing fields {missing_fields}.'
                      ' Please pass the missing fields either in a yaml file or as command line arguments.')
            missing_fields_string = ', '.join(missing_fields)
            raise Exception(f'Cannot construct RunModel with missing fields: {missing_fields_string}')

        # Fill in default initial values for RunModel
        model_as_dict.update({
            'run_id': str(uuid.uuid4()),
        })

        return cls(**model_as_dict)


@dataclass
class PartialRunModel:
    """ Partial Run Model """
    name: Optional[str] = None
    git_branch: Optional[str] = None
    git_repo: Optional[str] = None
    image: Optional[str] = None
    instance: Optional[str] = None

    # Generated unless otherwise provided
    command: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    @classmethod
    def empty(cls) -> PartialRunModel:
        return cls()

    def merge(self, other: PartialRunModel) -> PartialRunModel:
        """Flat merges a PartialRunModel into another and returns the result

        Args:
            other: The PartialRunModel to override the called PartialRunModel
                for non empty values

        Returns:
            A generated new merged PartialRunModel
        """
        new_prm = PartialRunModel.empty()
        for field in fields(PartialRunModel):
            if getattr(other, field.name) is not None:
                other_value = getattr(other, field.name)
                setattr(new_prm, field.name, other_value)
            else:
                original_value = getattr(self, field.name)
                setattr(new_prm, field.name, original_value)
        return new_prm

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> PartialRunModel:
        """Load the config from the provided YAML file.

        Args:
            path (Union[str, Path]): Path to YAML file

        Returns:
            PartialRunModel: The PartialRunModel object specified in the YAML file
        """
        # TODO: support loading the yaml with inheritence
        # Will likely use yamlmerge (see: https://github.com/mosaicml/yahp/issues/91)
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False) -> PartialRunModel:
        """Load the config from the provided dictionary.

        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the PartialRunModel with

        Returns:
            PartialRunModel: The PartialRunModel object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}
        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value
            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            warnings.warn(f'Encountered fields {unused_keys} which were not used in constructing the run.')

        return cls(**constructor)
