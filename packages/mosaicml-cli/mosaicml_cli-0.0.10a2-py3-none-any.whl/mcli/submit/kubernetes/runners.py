""" Generic Runner for MCLI K8s Jobs """
from typing import Optional

from kubernetes import client, config
from kubernetes.client import ApiClient

from mcli.submit.kubernetes.mcli_job import MCLIJob
from mcli.submit.kubernetes.merge import merge
from mcli.submit.platforms.registry import PlatformRegistry


def title_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


class Runner:
    """ Generic Runner for MCLI K8s Jobs """

    def __init__(self, platform_registry: Optional[PlatformRegistry] = None):
        self.platform_registry = platform_registry if platform_registry else PlatformRegistry.from_default_config()

    def get_specs(self, job: MCLIJob, instance: str, attach_ebs: bool = False, priority_class: Optional[str] = None):
        platform = self.platform_registry.get_for_instance_type(instance)

        job_platform_spec, other_platform_specs, shared_platform_metadata = platform.get_specs(
            instance, attach_ebs, priority_class=priority_class)
        job_base_spec, other_specs, shared_job_metadata = job.get_specs()

        api = ApiClient()

        job_spec = merge(api.sanitize_for_serialization(job_platform_spec),
                         api.sanitize_for_serialization(job_base_spec))

        # Sanitize other specs
        other_specs = [api.sanitize_for_serialization(other_spec) for other_spec in other_platform_specs + other_specs]

        # Add shared metadata
        shared_metadata = merge(api.sanitize_for_serialization(shared_platform_metadata),
                                api.sanitize_for_serialization(shared_job_metadata))

        for spec in [job_spec] + other_specs:
            merge(spec, {'metadata': shared_metadata})

            # Add shared metadata to template specs (ie pods)
            if 'spec' in spec and 'template' in spec['spec']:
                merge(spec['spec']['template'], {'metadata': shared_metadata})

        return other_specs + [job_spec]

    # TODO(Niklas): deprecate attach_ebs.
    def submit(self, job: MCLIJob, instance: str, attach_ebs: bool = False, priority_class: Optional[str] = None):
        specs = self.get_specs(job, instance, attach_ebs, priority_class)
        platform = self.platform_registry.get_for_instance_type(instance)
        api_client = config.new_client_from_config(context=platform.context_name)

        for spec in specs:
            # Get API client from the object api version string.
            # E.g. "batch/v1" => client.BatchV1Api()
            api_version_str = spec['apiVersion']
            api_version_fragments = api_version_str.split('/')
            if len(api_version_fragments) > 1:
                api_name, api_version = api_version_fragments[:2]
            else:
                api_name, api_version = ('Core', api_version_fragments[0])
            api_name = api_name.capitalize() + api_version.upper() + 'Api'
            api = getattr(client, api_name)
            api = api(api_client=api_client)

            # Find corresponding create method from Kind string.
            # e.g. "Job" => api.create_namespaced_job(...)
            kind_str = spec['kind']
            create = getattr(api, f'create_namespaced_{title_to_snake(kind_str)}')
            create(platform.namespace, body=spec)
