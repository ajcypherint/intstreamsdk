from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource

TRAFFIC = "traffic"
MITIGATED = "mitigated"


class IPv4AutoMitigateJob(IndicatorJob):
    def __init__(self, client_class):
        super(IPv4AutoMitigateJob, self).__init__(client_class)

    def custom(self, parsed_args):

        # get indicator data
        ip_resource = resource.IPV4(self.client)
        ip_resource.filter({"value": parsed_args.indicator})
        res = ip_resource.full_request()
        indicators = res["data"]["results"]
        # if indicator found
        if len(indicators) > 0:
            indicator_id = indicators[0]["id"]
            ########
            # insert mitigation code here.
            # if successful set mitigated
            ########
            # update indicator and set mitigated = True
            put_resource = resource.IPV4(self.client, resource.Resource.PUT)
            put_resource.id(indicator_id)
            indicator_data = indicators[0]
            if not indicator_data.get(MITIGATED, False):
                indicator_data[MITIGATED] = True
                put_resource.indicators_put(indicator_data)
                put_resource.full_request()


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = IPv4AutoMitigateJob(SyncClient)
    # add any
    demo.run()
