# pylint: disable=duplicate-code

""" The GCP Platform """

from mcli.submit.platforms_future.gcp_instances import GCP_INSTANCE_LIST
from mcli.submit.platforms_future.instance_type import InstanceList
from mcli.submit.platforms_future.platform import GenericK8sPlatform


class GCPPlatform(GenericK8sPlatform):
    """ The GCP Platform """

    allowed_instances: InstanceList = GCP_INSTANCE_LIST
