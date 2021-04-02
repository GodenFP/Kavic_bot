# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()
scopes = ["https://www.googleapis.com/auth/youtube"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "yt" + sep + "client_secret_427484376462-65dei1asn0agbi847s415thvi41i678b.apps.googleusercontent.com.json"
plid = "PLQu61FekieSStFTy3f3YIEvBy7xo2Yqho"

def init():
    # Get credentials and create an API client
    try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
    except:
        print('client_secrets_file not found.')
        
    credentials = flow.run_console()
    
    youtube = googleapiclient.discovery.build(
                api_service_name,
                api_version,
                credentials = credentials
            )
    return youtube

def check_list(youtube, num):

    request = youtube.playlistItems().list(
        part = "snippet,contentDetails",
        maxResults = num,
        playlistId = plid
    )
    response = request.execute()
    return response
    

def add_song(youtube, vid):

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId" : plid,
            #"position" : 0,
            "resourceId" : {
              "kind" : "youtube#video",
              "videoId" : vid
            }
          }
        }
    )
    response = request.execute()

    print(response)

def delete_song(youtube, plit_id):
    
    request = youtube.playlistItems().delete(
        id = plit_id
    )
    request.execute()

def get_url_by_title(target):
    
    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey = 'AIzaSyCSuQE5KLziIu9kmFr2TcRkujXsPhHPjXU'
    )

    request = youtube.search().list(
        part = "snippet",
        maxResults = 1,
        q = str(target)
    )
    response = request.execute()

    url = response['items'][0]['id']['videoId']
    return url

def delete_num_songs(youtube, num):
    try:
        items = check_list(youtube, num)['items']
        for item in items:
            delete_song(youtube, item['id'])
        
        print('update successful')
    except:
        print('something wrong when deleting songs')
        
def add_num_songs(youtube, num):
    r = []
    with open('list' + sep + 'song_list.txt', encoding = 'utf-8') as File:
        r = File.read().split('\n')
        while '' in r:
            r.remove('')
        print(r)
        for i in range(0, num):
            choice = random.choice(r)
            print(choice)
        
            add_song(youtube, choice)
            r.remove(choice)
        
    with open('list' + sep + 'song_list.txt', 'w', encoding = 'utf-8') as File:
        for line in r:
            File.write(line + '\n')

def update_song_list(num):
    youtube = init()
    
    delete_num_songs(youtube, num)
    add_num_songs(youtube, num)

def add_to_song_list(num):
    youtube = init()
    add_num_songs(youtube, num)

def delete_from_song_list(num):
    youtube = init()
    delete_num_songs(youtube, num)
