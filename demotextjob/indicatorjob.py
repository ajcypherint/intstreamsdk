from intstreamsdk.job import IndicatorJob
from intstreamsdk.client import SyncClient
from intstreamsdk import resource


class CatJob(IndicatorJob):
    def __init__(self, client_class):
        super(CatJob, self).__init__(client_class)

    def custom(self, parsed_args):
        # retrieve id
        netloc = parsed_args.indicator
        # get indicator id
        uploader = resource.DomainLoader([netloc], self.client)
        data = uploader.upload()
        indicator_id = data[0]["id"]

        # set category
        COL = "category"
        upsert = resource.ColumnGetPerform(self.client)
        # here query some system to get the category
        category = "Business; Technology"
        # save to databasennn
        upsert.upsert(resource.IndicatorTextField, COL, category, indicator_id)


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = CatJob(SyncClient)
    # add any
    demo.run()