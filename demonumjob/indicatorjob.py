from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource
import random


class IPv4Job(IndicatorJob):
    def __init__(self, client_class):
        super(IPv4Job, self).__init__(client_class)

    def custom(self, parsed_args):
        # retrieve id
        ipv4 = parsed_args.indicator
        data = self.check_upload([ipv4], resource.IPV4)
        indicator_id = data[0]["id"]

        COL = "traffic"
        upsert = resource.ColumnGetPerform(self.client)
        # here query some system to get the traffic count.
        traffic_count = random.randint(0,2)
        # save to databasennn
        upsert.upsert(resource.IndicatorNumericField, COL, traffic_count, indicator_id)


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = IPv4Job(SyncClient)
    # add any
    demo.run()
