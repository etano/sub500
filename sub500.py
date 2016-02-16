import string
from random import choice, randint
import tweepy, time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

f = open('ytAuth.txt','r')
lines = [x.rstrip() for x in f.readlines()]
DEVELOPER_KEY = lines[0]
CLIENT_ID = lines[1]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def FilterFeed(items):
  vids = []
  for entry in items:
    if entry['statistics'] != None:
      view_count = int(entry['statistics']['viewCount'])
    else:
      view_count = 0
    if view_count < 500: # Sub 500
      id = entry['id']
      url = 'http://www.youtube.com/watch?v='+id
      title = entry['snippet']['title']
      vids.append([id,url,title,view_count])
  if vids != []:
    return choice(vids)
  else:
    return None

def SearchYoutube(search_terms):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=search_terms.encode('ascii','ignore'),
    part="id",
    maxResults=50,
    order="date",
    safeSearch="none",
    type="video"
  ).execute()

  search_videos = []
  for search_result in search_response.get("items", []):
    search_videos.append(search_result["id"]["videoId"])
  video_ids = ",".join(search_videos)

  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, statistics'
  ).execute()

  return FilterFeed(video_response.get("items", []))

def GetSub500():
  # Get words
  f = open('words.txt','r')
  words = []
  for line in f:
    word = line.rstrip().decode('utf-8')
    words.append(word)

  vid = None
  while vid == None:
    word = choice(words)
    vid = SearchYoutube(word)
  return vid

f = open('twitterAuth.txt','r')
lines = [x.rstrip() for x in f.readlines()]
CONSUMER_KEY = lines[0] # To get this stuff, sign in at https://dev.twitter.com/ and Create a New Application
CONSUMER_SECRET = lines[1] # Make sure access level is Read And Write in the Settings tab
ACCESS_KEY = lines[2] # Create a new Access Token
ACCESS_SECRET = lines[3] # Shhhhhhhhh....
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

Going = True
while Going:
    [id,url,title,view_count] = GetSub500()
    print id, url, title, view_count
    api.update_status('('+str(view_count)+') '+title+': '+url)
    time.sleep(10800) # Sleep for 3 hours
