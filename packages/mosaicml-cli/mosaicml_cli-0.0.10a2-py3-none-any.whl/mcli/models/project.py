""" The Project Model object that comes directly from GraphQL """
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from mcli import config
from mcli.api.schema.generic_model import DeserializableModel


@dataclass
class ProjectModel(DeserializableModel):
    """ The Project Model object that comes directly from GraphQL """

    project: str
    created_by: str
    image: str
    repo: str
    branch: str
    creation_time: datetime
    last_update_time: datetime

    # Used for renaming projects
    new_project_name: Optional[str] = field(default=None,)

    # Used for renaming projects
    new_project_name: Optional[str] = field(default=None,)

    property_translations = {
        'projectName': 'project',
        'createdBy': 'created_by',
        'lastUpdatedTimestamp': 'last_update_time',
        'creationTimestamp': 'creation_time',
    }

    def to_create_project_data(self) -> Dict[str, Any]:
        return {
            'projectName': self.project,
            'createdBy': self.created_by,
            'image': self.image,
            'repo': self.repo,
            'branch': self.branch,
        }

    def to_update_project_data(self) -> Dict[str, Any]:
        data = self.to_create_project_data()
        data['newProjectName'] = self.new_project_name
        return data

    def create_featuredb(self) -> bool:
        """Creates the ProjectConfig in FeatureDB

        Should only be called once

        Return:
            Returns true if successful
        """
        if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
            # pylint: disable-next=import-outside-toplevel
            from mcli.api.projects.create_project import create_project
            return create_project(self)
        return True
