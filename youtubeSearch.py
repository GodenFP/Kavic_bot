# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_url_by_title(target):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_427484376462-8l3us49583g1l0r1n0lrj8v191v56qp2.apps.googleusercontent.com.json"
    
    
    # Get credentials and create an API client
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version,
        developerKey = 'AIzaSyCSuQE5KLziIu9kmFr2TcRkujXsPhHPjXU')

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=str(target)
    )
    response = request.execute()

    url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']
    return url
