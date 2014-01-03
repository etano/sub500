import string
from random import choice, randint
import tweepy, time
import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()

# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
yt_service.ssl = True
f = open('ytAuth.txt','r')
lines = [x.rstrip() for x in f.readlines()]
yt_service.developer_key = lines[0]
yt_service.client_id = lines[1]

def FilterFeed(feed):
  vids = []
  for entry in feed.entry:
    if entry.statistics != None:
      view_count = int(entry.statistics.view_count)
    else:
      view_count = 0
    if view_count < 500: # Sub 500
      id = entry.id.text.split('/')[-1]
      url = 'http://www.youtube.com/watch?v='+id
      title = entry.media.title.text
      vids.append([id,url,title,view_count])
  if vids != []:
    return choice(vids)
  else:
    return None

def SearchYoutube(search_terms):
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.vq = search_terms.encode('ascii','ignore')
  query.max_results = 50
  query.racy = 'include'
  feed = yt_service.YouTubeQuery(query)
  return FilterFeed(feed)

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
