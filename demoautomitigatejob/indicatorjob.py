from intstreamsdk.client import SyncClient
from intstreamsdk import mitigate, resource

TRAFFIC = "traffic"

#####
# TODO: Edit the resource model for indicator type you want to mitigate:
# IPV4, IPV6, Sha1, Sha256, MD5, NetLoc
#######


class AutoIPV4MitigateJob(mitigate.MitigateJob):
    def __init__(self, client_class, ):
        super(AutoIPV4MitigateJob, self).__init__(client_class, mitigate.RESOURCE_IPV4)

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
            if data[0].get("value") == 0:
                return True
        return False


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = AutoIPV4MitigateJob(SyncClient)
    # add any
    demo.run()
