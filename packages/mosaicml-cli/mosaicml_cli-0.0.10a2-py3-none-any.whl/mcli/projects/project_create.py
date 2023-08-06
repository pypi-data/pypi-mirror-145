""" Project Creation """
import copy
import getpass
from datetime import datetime
from typing import Optional

from mcli import config
from mcli.platform.platform_info import get_platform_list
from mcli.projects.project_config import ProjectConfig
from mcli.projects.project_modify import (configure_branch, configure_docker_image, configure_project_name,
                                          configure_repo)


def create_new_project_from_template(template_project: ProjectConfig) -> ProjectConfig:
    new_project: ProjectConfig = copy.deepcopy(template_project)
    new_project.project = configure_project_name(name=new_project.project)
    new_project.image = configure_docker_image(image=new_project.image)
    new_project.repo = configure_repo(repo=new_project.repo)
    new_project.branch = configure_branch(branch=new_project.branch)
    new_project.last_update_time = datetime.now()
    return new_project


def get_default_project_config() -> ProjectConfig:
    default_username = None
    platform_list = get_platform_list()
    platform_names = [x.namespace for x in platform_list if x.namespace]
    if len(platform_names):
        default_username = platform_names[0]
    if not default_username:
        default_username = getpass.getuser()

    project = f'{default_username}-project'
    image = 'mosaicml/pytorch'
    repo = 'mosaicml/composer'
    branch = 'dev'
    last_used = datetime.now()

    return ProjectConfig(
        project=project,
        created_by=default_username,
        image=image,
        repo=repo,
        branch=branch,
        last_update_time=last_used,
        creation_time=datetime.now(),
    )


def generate_new_project(fork_from: Optional[ProjectConfig]) -> ProjectConfig:
    if fork_from is None:
        fork_from = get_default_project_config()

    assert fork_from is not None, 'Must have a valid default project to fork from'
    new_project = create_new_project_from_template(template_project=fork_from)
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        if new_project.create_featuredb():
            print('Persisted new project in FeatureDB')
    new_project.save()
    return new_project


def create_new_project(**kwargs) -> int:
    """Creates a new project forked from the current project and sets it as
    current

    Args:
        **kwargs:

    Returns:
        Exit Code
    """
    del kwargs
    current_project = ProjectConfig.get_current_project()
    current_project.project = ''
    new_project = create_new_project_from_template(template_project=current_project,)
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        if new_project.create_featuredb():
            print('Persisted new project in FeatureDB')
    new_project.save()
    new_project.set_current_project()

    return 0
