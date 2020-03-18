import calendar
import json
import re
import time
import pyperclip
import requests
from requests_oauthlib import OAuth1

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

URL = "https://stream.twitter.com/1.1/statuses/filter.json"


def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def set_clipboard(string):
    pyperclip.copy(string)


if __name__ == '__main__':
    word = input()

    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    r = requests.post(URL, auth=auth, stream=True, data={'track': word})

    for line in r.iter_lines():
        stream = line.decode("utf-8")
        try:
            tweet = json.loads(stream)
            text = tweet['text']
            print(YmdHMS(tweet['created_at']))
            print('ID:' + '@' + tweet['user']['screen_name'])
            match = re.findall(r'[0-9A-F]{8}', text)
            print(tweet['text'])
            if len(match) == 1:
                set_clipboard(match[0])
        except json.decoder.JSONDecodeError as e:

            pass
