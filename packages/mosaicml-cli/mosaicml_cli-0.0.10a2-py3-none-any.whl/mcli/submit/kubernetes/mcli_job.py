""" Kubernetes Intermediate Job Abstraction """
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Dict, List, Optional

import yaml
from kubernetes import client  # , config

from mcli import version
from mcli.utils.utils_kube_labels import label


@dataclass
class MCLIJob():
    """ Kubernetes Intermediate Job Abstraction """

    name: str = ''
    container_image: str = ''
    working_dir: str = ''
    command: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    ttl: int = int(timedelta(days=14).total_seconds())
    parameters: Dict[str, Any] = field(default_factory=dict)
    sweep: Optional[str] = None

    def get_specs(self):
        """
        Generates base kubernetes specs
        """
        other_specs = []

        job_spec = client.V1Job(api_version='batch/v1', kind='Job')
        job_spec.metadata = client.V1ObjectMeta(name=self.name)
        job_spec.status = client.V1JobStatus()

        env_list = []
        for env_name, env_value in self.environment.items():
            env_list.append(client.V1EnvVar(name=env_name, value=env_value))

        # Create the configmap spec
        data = yaml.dump({k: v for k, v in self.parameters.items() if not k.startswith('_')})
        cm = client.V1ConfigMap(api_version='v1', kind='ConfigMap', data={'parameters.yaml': data})
        cm.metadata = client.V1ObjectMeta(name=self.name)
        other_specs.append(cm)

        # Create the volume and volume mount
        cm_volume = client.V1Volume(name='config', config_map=client.V1ConfigMapVolumeSource(name=self.name))
        cm_mount = client.V1VolumeMount(name='config', mount_path='/mnt/config')

        container = client.V1Container(name='default',
                                       env=env_list,
                                       image=self.container_image,
                                       command=['/bin/bash', '-c'],
                                       args=self.command,
                                       volume_mounts=[cm_mount])

        template = client.V1PodTemplate()
        template.template = client.V1PodTemplateSpec()
        template.template.spec = client.V1PodSpec(containers=[container], volumes=[cm_volume])
        job_spec.spec = client.V1JobSpec(template=template.template, ttl_seconds_after_finished=self.ttl)

        labels = {
            label.mosaic.JOB: self.name,
            'type': 'mcli',
            label.mosaic.LAUNCHER_TYPE: 'mcli',
            label.mosaic.MCLI_VERSION: str(version.__version__),
            label.mosaic.MCLI_VERSION_MAJOR: str(version.__version_major__),
            label.mosaic.MCLI_VERSION_MINOR: str(version.__version_minor__),
            label.mosaic.MCLI_VERSION_PATCH: str(version.__version_patch__),
        }
        if self.sweep:
            labels['mosaicml.com/sweep'] = self.sweep
        shared_metadata = client.V1ObjectMeta(labels=labels)

        return [job_spec, other_specs, shared_metadata]
