from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource
import random

TRAFFIC = "traffic"
MITIGATED = "mitigated"

#####
# TODO: Edit the resource model for indicator type you want to mitigate:
# IPV4, IPV6, Sha1, Sha256, MD5, NetLoc
#######
MODEL = "IPV4"


class AutoMitigateJob(IndicatorJob):
    def __init__(self, client_class):
        super(AutoMitigateJob, self).__init__(client_class)

    def do_mitigate(self, indicator):
        """
        TODO: EDIT This method; return True to mitigate indicator
        all column data will be updated when this script runs.
        :param indicator: dict indicator object
        :return:  bool
        """

        indicator_id = indicator["id"]
        num_fields_resource = resource.IndicatorNumericField(self.client)
        column_data = num_fields_resource.getIndicatorColumns(indicator_id)
        # retrieve traffic column
        data = [d for d in column_data if d["name"] == TRAFFIC]
        # if traffic column found
        if len(data) > 0:
            # if no traffic then mitigate
            if data[0].get("value", 0) == 0:
                return True
        # fake a result for now
        # return False
        return bool(random.getrandbits(1))

    def custom(self, parsed_args):
        """
        DO NOT EDIT
        :param parsed_args:
        :return:
        """

        # get indicator data
        ip_resource = getattr(resource, MODEL)(self.client)
        ip_resource.filter({"value": parsed_args.indicator})
        res = ip_resource.full_request()
        indicators = res["data"]["results"]
        # if indicator found
        if len(indicators) > 0:
            indicator = indicators[0]
            indicator_id = indicator["id"]
            do_mitigate = self.do_mitigate(indicator)
            if indicator.allowed:
                do_mitigate = False
            if do_mitigate:
                put_resource = getattr(resource,MODEL)(self.client, resource.Resource.PUT)
                put_resource.id(indicator_id)
                indicator_data = indicators[0]
                if not indicator_data[MITIGATED]:
                    indicator_data[MITIGATED] = True
                    put_resource.indicators_put(indicator_data)
                    put_resource.full_request()


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = AutoMitigateJob(SyncClient)
    # add any
    demo.run()
