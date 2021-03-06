# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from _simple_func import sep

scopes = ["https://www.googleapis.com/auth/youtube"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

# put client secret.json here
client_secrets_file = "Data" + sep + "personal_data" + sep \
                      + "client_secret_427484376462-65dei1asn0agbi847s415thvi41i678b.apps.googleusercontent.com.json"
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
                credentials=credentials
            )
    return youtube


def check_song_list(youtube, num):

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=num,
        playlistId=plid
    )
    response = request.execute()
    return response
    

def add_song(youtube, vid):

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": plid,
            # "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": vid
            }
          }
        }
    )
    response = request.execute()

    print(response)


def delete_song(youtube, plit_id):
    
    request = youtube.playlistItems().delete(
        id=plit_id
    )
    request.execute()


def get_url_by_title(target):
    
    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey='AIzaSyCSuQE5KLziIu9kmFr2TcRkujXsPhHPjXU'
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=str(target)
    )
    response = request.execute()

    url = response['items'][0]['id']['videoId']
    return url


def delete_num_songs(youtube, num):
    try:
        items = check_song_list(youtube, num)['items']
        for item in items:
            delete_song(youtube, item['id'])
        
        print('update successful')
    except:
        print('something wrong when deleting songs')
        

def add_num_songs(youtube, num):
    with open('Data' + sep + 'song_list.txt', encoding='utf-8') as File:
        r = File.read().split('\n')
        while '' in r:
            r.remove('')
        print(r)
        for i in range(0, num):
            choice = random.choice(r)
            print(choice)
        
            add_song(youtube, choice)
            r.remove(choice)
        
    with open('Data' + sep + 'song_list.txt', 'w', encoding='utf-8') as File:
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

    
def song_options(message):
    '''Add songs to song_list,
    Delete songs from song_list,
    or just search songs.
    Return a list of texts to be sent.
    '''
    send_text = []
    with open('Data' + sep + 'song_list.txt', 'r') as txt_file:
        song_list = txt_file.read().split('\n')
            
    num = len(song_list)
    for title in message[message.find(' ') + 1:].split(','):
        if title.startswith('https://www.youtube.com/'):
            if 'list' in title:
                send_text.append('??????list???:(')
                return send_text
            if title in song_list:
                send_text.append('U????????????!')
                return send_text
            song_list.append(title)
        elif title != '':
            url = get_url_by_title(title)
            if url in song_list:
                send_text.append('U????????????!')
                return send_text
            
            if message.startswith('-a ') or message.startswith('add '):
                song_list.append(url)
            elif message.startswith('-s ') or message.startswith('search '):
                send_text.append('https://youtu.be/' + url)
            elif message.startswith('-d ') or message.startswith('delete '):
                song_list.remove(url)

    with open('Data' + sep + 'song_list.txt', 'w', encoding='utf-8') as txt_file:
        for line in song_list:
            if line != '':
                txt_file.write(line + '\n')
                        
    # num of sent songs or deleted songs
    if message.startswith('-a ') or message.startswith('add '):
        send_text.append('You?????? ' + str(len(song_list) - num) + u' ???song(s) :)')
    if message.startswith('-d ') or message.startswith('delete '):
        send_text.append('You?????? ' + str(num - len(song_list)) + u' ???song(s) :(')
        
    # retun text list to send
    return send_text

# update_song_list(6)
