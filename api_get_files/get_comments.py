import os
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

request = youtube.comments().list(
    part="id,snippet",
    id="O2qjyrP_F_s"
)
response = request.execute()

print(response)

# if __name__ == "__main__":
#     main()