# pylint: disable=duplicate-code

""" The AWS Platform """

from mcli.submit.platforms_future.aws_instances import AWS_INSTANCE_LIST
from mcli.submit.platforms_future.instance_type import InstanceList
from mcli.submit.platforms_future.platform import GenericK8sPlatform


class AWSPlatform(GenericK8sPlatform):
    """ The AWS Platform """

    allowed_instances: InstanceList = AWS_INSTANCE_LIST
