""" Run Pipeline for singular runs """
import logging
import uuid
from dataclasses import asdict
from typing import Optional

from mcli.models.run import PartialRunModel, RunModel
from mcli.submit.kubernetes.mcli_job_future import MCLIJob
from mcli.utils.utils_config import format_jinja

log = logging.getLogger(__name__)


def create_partial_run_models(file: Optional[str] = None,) -> PartialRunModel:

    prm = PartialRunModel.empty()

    if file is not None:
        log.info(f'Loading config from file {file}')
        file_model = PartialRunModel.from_file(file)
        prm = prm.merge(file_model)

    return prm


def mcli_job_from_run_model(run_model: RunModel) -> MCLIJob:
    formatted_command = format_jinja(run_model.command, asdict(run_model))

    return MCLIJob(
        name=f'{run_model.name}-{str(uuid.uuid4())[0:4]}',
        container_image=run_model.image,
        command=[formatted_command],
        parameters=run_model.parameters,
    )
