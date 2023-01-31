'''
Gets playlistId for a channel, using channel id.
In this case the playlistId is the full collection of videos, not a regular YouTube playlist.
Then gets YouTube videos within that full playlist.

!!! Note that each request to the channels endpoint costs 1 quota !!!
!!! Note that each request to the playlists endpoint costs 1 quota !!!

'''

# Imports
# -------
import os
import datetime as dt
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors

from config import *
#TODO incorporate logging

# API Setup
# ---------
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

# Paths and Keys
# --------------
cwd = os.getcwd()
time = dt.datetime.now().strftime('%Y%m%d_%H%M')
filepath = f'{cwd}/outputs/output_{time}.csv'

DEVELOPER_KEY = os.environ['DEVELOPER_KEY']

# Search parameters
# -----------------
part = "snippet"
# channelIds = channelIds #DonaldJTrumpforPresident

# max results per page; max=50, min=0, default=5
results_per_page = 50


# ----------------------------------------------------------------------------------------------------------------------

def run_channels_request(youtube, channelId, results_per_page, nextPageToken):
    '''
    Returns request for channel playlist id (from channel id)
    '''

    request = youtube.channels().list(
        part="contentDetails",
        id=channelId,
        maxResults=results_per_page,
        pageToken=nextPageToken
    )

    return request


def run_playlist_items_request(youtube, part, playlistId, results_per_page, nextPageToken):
    '''
    Returns request for playlist items
    '''

    request = youtube.playlistItems().list(
        part=part,
        playlistId=playlistId,
        maxResults=results_per_page,
        pageToken=nextPageToken
    )

    return request


def process_search_results(response_items):
    df = pd.DataFrame(response_items)
    dfs = []
    for column in df.columns:
        col_exp = pd.json_normalize(df[column])
        dfs.append(col_exp)
    full_df = pd.concat(dfs, axis=1)

    return full_df


def main():
    '''
    The first part of this code sends a request to the chosen YouTube endpoint and gets the first page of results. The
    nextPageToken is then used to paginate though subsequent pages.

    Each page of results is written/appended to a csv file at the specified location.
    '''
    # TODO why is header occurring for second channel id?
    id_count = 1
    for channelId in channelIds:
        id_count = id_count + 1
        # TODO can I put username in here too?
        print('--------------------------------------------------------------------------------------------------')
        print(f'\nCollecting videos from {channelId}')
        try:
            # Get credentials and create an API client
            youtube = googleapiclient.discovery.build(
                api_service_name,
                api_version,
                developerKey=DEVELOPER_KEY)

            nextPageToken = None

            # Get playlistID for channel using channelID
            request = run_channels_request(youtube, channelId, results_per_page, nextPageToken)
            response = request.execute()

            playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


            # Initial search (first page of results)
            request = run_playlist_items_request(youtube, part, playlistId, results_per_page, nextPageToken)

            # Get response from request
            response = request.execute()
            response_items = response['items']

            # Process data and save to csv
            full_df = process_search_results(response_items)
            videos_columns = full_df.columns

            if id_count > 1:
                mode = 'a'
                header = True
            else:
                mode = 'w'
                header = False

            full_df.to_csv(f'{filepath}', mode=mode, index=False, header=header)

            # Print updates
            if len(response_items) < results_per_page:
                result_count = len(response_items)
            else:
                result_count = results_per_page
            print(f'\n{len(response_items)} rows collected. Total results: {result_count}')

            # Set nextPageToken
            nextPageToken = response.get('nextPageToken')

            # Use nextPageToken to paginate through subsequent pages
            # TODO pages after 50 have a different order???
            while nextPageToken:
                request = run_playlist_items_request(youtube, part, playlistId, results_per_page, nextPageToken)

                response = request.execute()
                response_items = response['items']

                # Set nextPageToken
                nextPageToken = response.get('nextPageToken')

                # Process data and  append to csv
                full_df = process_search_results(response_items)
                full_df = full_df[videos_columns]
                full_df.to_csv(f'{filepath}', mode='a', index=False, header=False)

                # Print results
                if len(response_items) < results_per_page:
                    result_count = len(response_items) + result_count
                else:
                    result_count = results_per_page + result_count
                print(f'\n{len(response_items)} rows collected. Total results: {result_count}')

            print("\nSearch complete!")
            print(f"\nResults saved to {filepath}")

        except Exception as e:
            print(e)
            if '403' in str(e):
                print("\nQuota exceeded! Exiting...")
            exit()


if __name__ == "__main__":
    main()