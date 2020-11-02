# demo class and main below.
# server side will pass access and refresh instead.
# server side then calls run with kwargs
from intstreamsdk.job import Job
import os
from intstreamsdk.client import AsyncClient, SyncClient
from intstreamsdk import extract
from intstreamsdk import resource
import argparse


class IPv4Job(Job):
    def __init__(self, client_class):
        super(IPv4Job, self).__init__(client_class)

    def custom(self, parsed_args):
        ipv4 = parsed_args.indicator
        # get indicator
        # set custom field


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = IPv4Job(SyncClient)
    # add any
    demo.parser.add_argument("--file", type=str, required=True)
    demo.run()