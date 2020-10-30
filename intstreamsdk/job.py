from intstreamsdk import resource, client
import os
import argparse


class Job(object):
    def __init__(self,
                 client_class,
                 format=client.Client.FORMAT_JSON
                 ):
        username = os.environ.get("JOB_USERNAME", None)
        password = os.environ.get("JOB_PASSWORD", None)
        server_url = os.environ.get("JOB_SERVER_URL", None)
        # below for server usage
        access = os.environ.get("JOB_ACCESS", None)
        refresh =  os.environ.get("JOB_REFRESH", None)

        self.client = client_class(username=username,
                                 password=password,
                                 server_url=server_url,
                                 access=access,
                                 refresh=refresh,
                                 format=format
                                 )
        self.parser = argparse.ArgumentParser()

    def custom(self, parsed_args):
        raise NotImplemented

    def check_upload(self,
                     indicators,
                     resource_class,
                     ):
        uploader = resource.Uploader(self.client)
        return uploader.check_upload(indicators, resource_class)

    def run(self):
        args = self.parser.parse_args()
        self.custom(args)
