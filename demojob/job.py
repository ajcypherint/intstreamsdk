# demo class and main below.
# server side will pass access and refresh instead.
# server side then calls run with kwargs
from intstreamsdk.job import Job
import os
from intstreamsdk.client import AsyncClient, SyncClient
from intstreamsdk import extract
from intstreamsdk import resource
import argparse
import ipaddress

# demo class and main below.
# server side will pass access and refresh instead.
# server side then calls run with kwargs





class ExtractJob(Job):
    def __init__(self, client_class):
        super(ExtractJob,self).__init__(client_class)

    def custom(self, parsed_args):
        # see /tests/integration.py for examples
        # self.client - Intstream client
        uploader = None
        with open(parsed_args.file, "r", encoding="utf8") as f:
            text = f.read()
            f.flush()
            #demo upload indicators
            # !!instead just set extract_indicators on source!!


            indicators = extract.extract_all(text)

            md5_data = self.check_upload(indicators["md5"], resource.MD5)
            sha1_data = self.check_upload(indicators["sha1"], resource.SHA1)
            sha256_data = self.check_upload(indicators["sha256"], resource.SHA256)
            email_data = self.check_upload(indicators["email"], resource.Email)
            ipv4_data = self.check_upload(indicators["ipv4"], resource.IPV4)
            compressed_ipv6s = [ipaddress.IPv6Address(i).compressed for i in indicators["ipv6"]]
            ipv6_data = self.check_upload(compressed_ipv6s, resource.IPV6)
            # no url indicator; domain instead
            uploader = resource.DomainLoader(indicators["url"], self.client)
            netloc_data = uploader.upload()
            # reset to start of file
            # demo upload html article
            resource_raw = resource.RawArticle(self.client, method=resource.Resource.POST)
            resource_raw.article_post(title="article test", source_id=1, text=text)
            response_raw = resource_raw.full_request()

            indicators_ids = []
            indicators_ids.extend([i["id"] for i in netloc_data])
            indicators_ids.extend([i["id"] for i in email_data])
            indicators_ids.extend([i["id"] for i in md5_data])
            indicators_ids.extend([i["id"] for i in sha1_data])
            indicators_ids.extend([i["id"] for i in sha256_data])
            indicators_ids.extend([i["id"] for i in ipv4_data])
            indicators_ids.extend([i["id"] for i in ipv6_data])
            resource_link = resource.Link(self.client,
                                          method=resource.Resource.POST,
                                          article_id=response_raw["data"]["id"],
                                          indicator_ids=indicators_ids)
            resource_link.full_request()


if __name__ == "__main__":
    # set env variables:
    # JOB_USERNAME
    # JOB_PASSWORD
    # JOB_SERVER_URL - base server url

    # initialize job object     with SyncClient or AsyncClient
    demo = ExtractJob(SyncClient)
    # add any
    demo.parser.add_argument("--file", type=str, required=True)
    demo.run()
