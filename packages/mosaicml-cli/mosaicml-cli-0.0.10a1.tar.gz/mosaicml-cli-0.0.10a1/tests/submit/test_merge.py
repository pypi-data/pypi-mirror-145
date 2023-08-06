""" Test Merge """
from kubernetes import client

from mcli.submit.kubernetes.merge import merge


def test_merge_dict():
    result = merge({'foo': 'bar'}, {'bar': 'baz'})
    assert len(result) == 2


def test_merge_dict_override():
    result = merge({'foo': 'bar'}, {'foo': 'baz'})
    assert len(result) == 1


def test_merge_dict_nested():
    result = merge({'foo': {'bar': 'baz'}}, {'foo': {'baz': 'gxz'}})
    assert len(result['foo']) == 2


def test_merge_lists():
    result = merge({'foo': [1]}, {'foo': [2]})
    assert len(result['foo']) == 2


def test_merge_lists_of_objects():
    result = merge({'foo': [{
        'name': 'foo',
        'x': 1
    }, {
        'name': 'bar'
    }]}, {'foo': [{
        'name': 'foo',
        'y': 1
    }, {
        'name': 'baz'
    }]})
    assert len(result['foo']) == 3


def test_merge_none_fields():
    result = merge({'foo': {'bar': None}}, {'foo': {'bar': 1.0}})
    assert result['foo']['bar'] == 1.0
    result = merge({'foo': {'bar': 1.0}}, {'foo': {'bar': None}})
    assert result['foo']['bar'] == 1.0


def test_merge():
    base = client.V1Job()
    other = client.V1Job()
    result = merge(base.to_dict(), other.to_dict())
    assert result is not None


def test_merge_containers():
    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    container = client.V1Container(name='default')
    template.template.spec = client.V1PodSpec(containers=[container])

    base = client.V1Job(spec=client.V1JobSpec(template=template.template))
    other = client.V1Job(spec=client.V1JobSpec(template=template.template))
    result = merge(base.to_dict(), other.to_dict())
    assert result is not None
    assert len(result['spec']['template']['spec']['containers']) == 1


def test_merge_environment():
    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    container = client.V1Container(name='default', env=[client.V1EnvVar(name='foo', value='bar')])
    template.template.spec = client.V1PodSpec(containers=[container])
    base = client.V1Job(spec=client.V1JobSpec(template=template.template))

    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    container = client.V1Container(name='default', env=[client.V1EnvVar(name='bar', value='baz')])
    template.template.spec = client.V1PodSpec(containers=[container])
    other = client.V1Job(spec=client.V1JobSpec(template=template.template))

    result = merge(base.to_dict(), other.to_dict())
    assert result is not None
    assert len(result['spec']['template']['spec']['containers']) == 1
    assert len(result['spec']['template']['spec']['containers'][0]['env']) == 2
