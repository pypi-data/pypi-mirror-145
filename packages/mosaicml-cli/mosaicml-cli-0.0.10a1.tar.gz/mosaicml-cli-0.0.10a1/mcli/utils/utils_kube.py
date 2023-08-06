"""Utils for automating K8s contexts"""
from __future__ import annotations

import base64
import copy
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Union, cast

from kubernetes import client, config


def get_client():
    config.load_kube_config()
    return client


def get_context():
    output = subprocess.getoutput('kubectl config current-context')
    return output


def kube_object_to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object returned by the Kubernetes API to a dict

    Args:
        obj (Kubernetes object): A Kubernetes object returned from the ``kubernetes.client``

    Returns:
        Dict[str, Any]: The serialized dictionary form of the ``obj``
    """
    api_client = client.ApiClient()
    return api_client.sanitize_for_serialization(obj)


@dataclass
class KubeContext():
    cluster: str
    user: str
    namespace: Optional[str] = None

    def __str__(self) -> str:
        return (f'cluster: {self.cluster},'
                f' \tuser: {self.user}, '
                f" \t{'namespace: ' + self.namespace if self.namespace else ''}")


def get_kube_contexts() -> List[KubeContext]:
    """Returns all configured K8s configured contexts

    Returns:
        List[KubeContext]: A list of the k8s contexts configured.
    """
    raw_contexts = config.list_kube_config_contexts()[0]
    raw_contexts = cast(List[Dict[str, Dict[str, str]]], raw_contexts)
    raw_contexts = [x['context'] for x in raw_contexts]
    contexts = [KubeContext(**x) for x in raw_contexts]
    return contexts


def get_current_context() -> KubeContext:
    """Returns the current K8s context

    Returns:
        KubeContext: The current K8s context
    """
    _, current_context = config.list_kube_config_contexts()

    return KubeContext(**current_context['context'])


# pylint: disable-next=invalid-name
def merge_V1ObjectMeta(*other: client.V1ObjectMeta) -> client.V1ObjectMeta:
    """ Merges a V1ObjectMeta into the Base V1ObjectMeta

    Does not handle lists such as `managed_fields` and `owner_references`

    Returns:
        A new V1ObjectMeta with the merged data
    """
    merged_meta = client.V1ObjectMeta()
    for attr in client.V1ObjectMeta.attribute_map:
        for o in other:
            if getattr(o, attr) is not None:
                found_attr = getattr(o, attr)
                if attr in ('labels', 'annotations') and getattr(merged_meta, attr):
                    base_labels: Dict[str, str] = getattr(merged_meta, attr)
                    base_labels.update(found_attr)
                    setattr(merged_meta, attr, base_labels)
                else:
                    setattr(merged_meta, attr, found_attr)
    return merged_meta


def safe_update_optional_list(
    original_value: Optional[List[Any]],
    additions: List[Any],
) -> List[Any]:
    """ Returns a copy with the merged optional list and additional list """
    if original_value is not None:
        return original_value + additions
    else:
        return copy.deepcopy(additions)


def safe_update_optional_dictionary(
    original_value: Optional[Dict[Any, Any]],
    additions: Dict[Any, Any],
) -> Dict[Any, Any]:
    """ Returns a copy with the merged optional dict and additional dict """
    if original_value is not None:
        new_dict = copy.deepcopy(original_value)
        new_dict.update(additions)
        return new_dict
    else:
        return copy.deepcopy(additions)


@contextmanager
def use_context(context: str) -> Generator[KubeContext, None, None]:
    """_summary_

    Args:
        context (str): Name of the context to use for Kubernetes API calls

    Raises:
        ValueError: if the requested context does not exist

    Yields:
        KubeContext: The KubeContext object for the current context
    """

    poss_contexts = [c for c in get_kube_contexts() if c.cluster == context]
    if len(poss_contexts) == 0:
        raise ValueError(f'No context named {context}')
    new_context = poss_contexts[0]

    previous_context = get_current_context()
    try:
        config.load_kube_config(context=new_context.cluster)
        yield new_context
    finally:
        config.load_kube_config(context=previous_context.cluster)


def base64_encode(message: str, encoding: str = 'utf-8') -> str:
    """Encode the provided message in base64

    Args:
        message (str): Message to encode
        encoding (str, optional): Byte encoding of `message`. Defaults to "utf-8".

    Returns:
        str: base64 encoded `message`
    """
    message_bytes = message.encode(encoding)
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode(encoding)
    return base64_message


def base64_decode(base64_message: str, encoding: str = 'utf-8') -> str:
    """Decode the provided base64-encoded message

    Args:
        base64_message (str): Message encoded in base64 to decode
        encoding (str, optional): Encoding that should be used for resulting message. Defaults to "utf-8".

    Returns:
        str: Decoded message
    """
    base64_bytes = base64_message.encode(encoding)
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode(encoding)
    return message


def read_secret(name: str, namespace: str) -> Optional[Dict[str, Union[str, Dict[str, Any]]]]:
    """Attempt to read the requested secret

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which to look

    Returns:
        Optional[Dict[str, str]]: If None, the secret does not exist. Otherwise, the secret is returned as a JSON.
    """
    api = client.CoreV1Api()
    try:
        secret = api.read_namespaced_secret(name=name, namespace=namespace)
        return kube_object_to_dict(secret)
    except client.ApiException:
        return None


def create_secret(
    name: str,
    namespace: str,
    data: Dict[str, str],
    secret_type: str = 'Opaque',
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> bool:
    """Create the requested secret

    Args:
        name: Name of the secret
        namespace: Namespace in which the secret should be created
        data: Secret data. Should be base64 encoded unless ``encode=True``.
        secret_type: Secret type. Defaults to "Opaque".
        labels: Additional labels that will be added to the secret, if provided.
        annotations: Additional annotations that will be added to the secret, if provided

    Returns:
        bool: True if creation succeeded
    """
    labels = labels or {}
    annotations = annotations or {}

    api = client.CoreV1Api()
    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    api.create_namespaced_secret(namespace=namespace, body=secret)
    return True


def update_secret(
    name: str,
    namespace: str,
    data: Dict[str, str],
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> bool:
    """Update the requested secret with new data

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which the secret exists
        data (Dict[str, str]): New secret data. Should be base64 encoded unless ``encode=True``.

    Returns:
        bool: True if update succeeded
    """

    # Get existing secret
    existing_secret = read_secret(name, namespace)
    if not existing_secret:
        raise client.ApiException(f'Could not find a secret named {name} within the namespace {namespace}')
    assert existing_secret is not None
    secret_type = existing_secret['type']

    labels = labels or {}
    annotations = annotations or {}

    api = client.CoreV1Api()
    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    api.patch_namespaced_secret(name, namespace, body=secret)
    return True


def list_secrets(namespace: str, labels: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
    """List all secrets in the namespace, filtered by labels

    Args:
        namespace (str): Kubernetes namespace
        labels (Optional[Dict[str, Optional[str]]]): Secret labels that must be matched. Defaults to None.

    Returns:
        Dict[str, Any]: Kubernetes secrets list as a JSON
    """
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    api = client.CoreV1Api()
    secrets = api.list_namespaced_secret(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(secrets)


def list_jobs(namespace: str, labels: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    api = client.BatchV1Api()
    jobs = api.list_namespaced_job(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(jobs)


def list_jobs_across_contexts(contexts: List[KubeContext],
                              labels: Optional[Dict[str, Optional[str]]] = None,
                              async_req: bool = True) -> List[Dict[str, Any]]:
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    job_requests = []
    for context in contexts:
        if context.namespace is None:
            print(f'No namespace for context {context.cluster}')
            continue
        with use_context(context.cluster):
            api = client.BatchV1Api()
            job_request = api.list_namespaced_job(namespace=context.namespace,
                                                  label_selector=label_selector,
                                                  async_req=async_req)
            job_requests.append(job_request)
    all_jobs = []
    for req in job_requests:
        jobs = req.get() if async_req else req
        all_jobs.extend(kube_object_to_dict(jobs)['items'])
    return all_jobs
