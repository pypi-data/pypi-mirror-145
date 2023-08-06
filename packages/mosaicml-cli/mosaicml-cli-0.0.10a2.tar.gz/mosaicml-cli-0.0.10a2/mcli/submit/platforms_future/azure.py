# pylint: disable=duplicate-code

""" The Azure Platform """

from mcli.submit.platforms_future.azure_instances import AZURE_INSTANCE_LIST
from mcli.submit.platforms_future.instance_type import InstanceList
from mcli.submit.platforms_future.platform import GenericK8sPlatform


class AzurePlatform(GenericK8sPlatform):
    """ The Azure Platform """

    allowed_instances: InstanceList = AZURE_INSTANCE_LIST
