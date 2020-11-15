from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource


class IPv4Job(IndicatorJob):
    def __init__(self, client_class):
        super(IPv4Job, self).__init__(client_class)

    def custom(self, parsed_args):
        ipv4 = parsed_args.indicator
        md5_data = self.check_upload([ipv4], resource.IPV4)
        indicator_id = md5_data[0]["id"]

        COL = "traffic"
        upsert = resource.ColumnGetPerform(self.client)
        # here query some system to get the traffic count.
        traffic_count = 1200
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