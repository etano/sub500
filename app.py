import sys
from random import choice

import tweepy
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


def filter_feed(items):
    vids = []
    for entry in items:
        view_count = 0
        if entry["statistics"] is not None:
            view_count = int(entry["statistics"]["viewCount"])
        if view_count < 500:  # Sub 500
            id = entry["id"]
            url = f"http://www.youtube.com/watch?v={id}"
            title = entry["snippet"]["title"]
            vids.append([id, url, title, view_count])
    return choice(vids) if vids else None


def search_youtube(youtube_client, search_terms):
    search_response = (
        youtube_client.search()
        .list(
            q=search_terms.encode("ascii", "ignore"),
            part="id",
            maxResults=50,
            order="date",
            safeSearch="none",
            type="video",
        )
        .execute()
    )
    search_videos = [result["id"]["videoId"] for result in search_response.get("items", [])]
    video_ids = ",".join(search_videos)
    video_response = youtube_client.videos().list(id=video_ids, part="snippet, statistics").execute()
    return filter_feed(video_response.get("items", []))


def get_sub500(youtube_client):
    with open("words.txt", "r") as f:
        words = [line.rstrip() for line in f]
    vid = None
    while vid is None:
        word = choice(words)
        vid = search_youtube(youtube_client, word)
    return vid


def main():
    google_developer_key = sys.argv[1]
    youtube_client = build("youtube", "v3", developerKey=google_developer_key)
    [id, url, title, view_count] = get_sub500(youtube_client)
    print(id, url, title, view_count)

    twitter_consumer_key = sys.argv[2]
    twitter_consumer_secret = sys.argv[3]
    twitter_access_key = sys.argv[4]
    twitter_access_secret = sys.argv[5]
    twitter_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    twitter_auth.set_access_token(twitter_access_key, twitter_access_secret)
    twitter_client = tweepy.API(twitter_auth)
    twitter_client.update_status(f"({view_count}) {title}: {url}")


if __name__ == "__main__":
    main()
