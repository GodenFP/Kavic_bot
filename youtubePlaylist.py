# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_427484376462-65dei1asn0agbi847s415thvi41i678b.apps.googleusercontent.com.json"
plid = 'PLQu61FekieSThVXZnWG7cLq2JRoOrBliX'#"PLQu61FekieSStFTy3f3YIEvBy7xo2Yqho"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    
credentials = flow.run_console()
    
youtube = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            credentials = credentials
        )

def check_list():

    request = youtube.playlistItems().list(
        part = "snippet,contentDetails",
        maxResults = 5,
        playlistId = plid
    )
    response = request.execute()
    return response
    

def add_song(vid):

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

def delete_song(plit_id):
    
    request = youtube.playlistItems().delete(
        id = plit_id
    )
    request.execute()

def delete_five_songs():
    try:
        items = check_list()['items']
        for item in items:
            delete_song(item['id'])
        
        print('update successful')
    except:
        print('something wrong when deleting songs')
        
def add_five_songs():
    r = []
    with open('list\\song_list.txt', encoding = 'utf-8') as File:
        r = File.read().split('\n')
        while '' in r:
            r.remove('')
        print(r)
        for i in range(0, 5):
            choice = random.choice(r)
            print(choice)
        
            add_song(choice)
            r.remove(choice)
        
    with open('list\\song_list.txt', 'w', encoding = 'utf-8') as File:
        for line in r:
            File.write(line + '\n')

def update_song_list():
    delete_five_songs()
    add_five_songs()


            

