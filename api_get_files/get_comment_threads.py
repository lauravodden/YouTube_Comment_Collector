'''

-*- coding: utf-8 -*-

Sample Python code for youtube.comments.list
See instructions for running these code samples locally:
https://developers.google.com/explorer-help/code-samples#python



'''

import os

import googleapiclient.discovery


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"

import os
import pandas as pd
import googleapiclient.discovery

# def main():
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['DEVELOPER_KEY']

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="id,snippet,replies",
    videoId="O2qjyrP_F_s"
)
response = request.execute()

print(response)


# if __name__ == "__main__":
#     main()