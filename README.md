sub500
======

Randomly selects videos with fewer than 500 views and sends them to [@sub500](https://twitter.com/sub500).

Get API info here: https://console.cloud.google.com/apis/credentials

To get started:

    sudo pip install tweepy
    sudo pip install --upgrade google-api-python-client
    python sub500.py

For crontab (every hour):

    0 * * * * /usr/bin/python /path/to/sub500/sub500.py >> /path/to/sub500/sub500.log 2>&1
