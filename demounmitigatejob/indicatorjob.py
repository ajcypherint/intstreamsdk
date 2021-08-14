from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource
from intstreamsdk import mitigate


class IPV4UnMitigateJob(mitigate.MitigateJob):
    def __init__(self, client_class):
        super(IPV4UnMitigateJob, self).__init__(client_class, mitigate.RESOURCE_IPV4)

    def do_mitigate(self, indicator):
        """
        your code goes here
        :param indicator:
        :return:
        """
        # api call to mitigation system here

        # if successful return True else False
        return True

if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = IPV4UnMitigateJob(SyncClient)
    # add any
    demo.run()
