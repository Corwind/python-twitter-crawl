#!/usr/bin/python3
"""
track.py

Usage:
    dump.py -k <keys_file> -w <words_file> -l <lang> -o <output>

Options:
    -h --help   Print this message
    --version   Print the version of this script
    -k          The file containing the keys for OAuth
    -w          The file containing the words to track
    -l          Language
    -o          The output file

© Systran
"""


import tweepy
from docopt import docopt
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


class SListener(StreamListener):

    def __init__(self, output):
        self.output = output
        StreamListener.__init__(self)

    def on_data(self, data):
        j = json.loads(data)
        if j is None:
            return False
        try:
            text = j['text']
        except KeyError:
            return False
        print(text)
        with open(self.output, "a") as o:
            json.dump(j, o, indent=4)
            o.close()
        return True

    def on_error(self, status):
        print(status)


def file_content(f):
    result = []
    with open(f) as f_open:
        for line in f_open:
            result.append(line)
    return result


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')

    keys = file_content(arguments['<keys_file>'])
    keys = [s.strip('\n') for s in keys]
    cons_key, cons_secret, access_token, access_secret = keys
    words = file_content(arguments['<words_file>'])
    words = [s.strip('\n') for s in words]
    lang = arguments['<lang>']
    auth = OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    tweetStream = Stream(auth, SListener(arguments['<output>']))
    tweetStream.filter(track=words, languages=[lang])
