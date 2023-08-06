""" Provides typing for Lazy Loaded MCLIK8sJob Class """
from typing import List, cast

from kubernetes import client


def get_empty_pod_template_spec() -> client.V1PodTemplateSpec:
    return client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(),
        spec=client.V1PodSpec(containers=[client.V1Container(name='DEFAULT')],),
    )


class MCLIK8sJobTyping(client.V1Job):
    """ Provides typing for Lazy Loaded MCLIK8sJob Class

    Makes properties and nested properties lazy loaded for convenience
    """

    @property
    def api_version(self) -> str:  # type: ignore
        if super().api_version:
            return cast(str, super().api_version)
        return 'batch/v1'

    @property
    def kind(self) -> str:  # type: ignore
        if super().kind:
            return cast(str, super().kind)
        return 'Job'

    @property
    def metadata(self) -> client.V1ObjectMeta:
        if self._metadata is None:
            self._metadata = client.V1ObjectMeta()
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: client.V1ObjectMeta) -> None:
        self._metadata = metadata

    @property
    def status(self) -> client.V1JobStatus:
        if self._status is None:
            self._status = client.V1JobStatus()
        return self._status

    @status.setter
    def status(self, status: client.V1JobStatus) -> None:
        self._status = status

    @property
    def spec(self) -> client.V1JobSpec:
        if self._spec is None:
            self._spec = client.V1JobSpec(template=get_empty_pod_template_spec())
        return self._spec

    @spec.setter
    def spec(self, spec: client.V1JobSpec) -> None:
        self._spec = spec

    @property
    def pod_spec(self) -> client.V1PodSpec:
        if self.spec.template is None:
            self.spec.template = get_empty_pod_template_spec()
        pod_template_spec = cast(client.V1PodTemplateSpec, self.spec.template)
        if pod_template_spec.spec is None:
            pod_template_spec.spec = client.V1PodSpec()
        return cast(client.V1PodSpec, pod_template_spec.spec)

    @pod_spec.setter
    def pod_spec(self, pod_spec) -> None:
        pod_template_spec = cast(client.V1PodTemplateSpec, self.spec.template)
        pod_template_spec.spec = pod_spec

    @property
    def container(self) -> client.V1Container:
        containers = cast(List[client.V1Container], self.pod_spec.containers)
        if len(containers) != 1:
            raise ValueError('MCLIK8sJobs can only have 1 container')
        return containers[0]

    @property
    def pod_volumes(self) -> List[client.V1Volume]:
        if self.pod_spec.volumes is None:
            self.pod_spec.volumes = []
        return self.pod_spec.volumes

    @pod_volumes.setter
    def pod_volumes(self, pod_volume: List[client.V1Volume]):
        self.pod_spec.volumes = pod_volume

    @property
    def container_volume_mounts(self) -> List[client.V1VolumeMount]:
        if self.container.volume_mounts is None:
            self.container.volume_mounts = []
        return self.container.volume_mounts

    @container_volume_mounts.setter
    def container_volume_mounts(self, container_volume_mount: List[client.V1VolumeMount]):
        self.container.volume_mounts = container_volume_mount

    @property
    def environment_variables(self) -> List[client.V1EnvVar]:
        if self.container.env is None:
            self.container.env = []
        return self.container.env

    @environment_variables.setter
    def environment_variables(self, environment_variables: List[client.V1EnvVar]):
        self.container.env = environment_variables

    @property
    def ports(self) -> List[client.V1ContainerPort]:
        if self.container.ports is None:
            self.container.ports = []
        return self.container.ports

    @ports.setter
    def ports(self, ports: List[client.V1ContainerPort]):
        self.container.ports = ports
