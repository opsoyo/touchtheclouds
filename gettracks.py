#!/usr/bin/python3

from __future__ import unicode_literals
import time
import json
import youtube_dl
import sys

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

request_stagger = 1.0

bdomain = 'https://soundcloud.com'

class ydl_logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        exit()
        if msg == 'axel exited with code 1':
            pass
        else:
            print(msg)

def ydl_hook(d):
    if d['status'] == 'finished':
        print('Download complete...{}'.format(d['filename']))

with open('profiles.json') as data_file:
    data = json.load(data_file)

for char in data:
    for profile in data[char]:
        #print('Working Profile: {}'.format(profile))
        sys.stdout.write("\x1b]2;Working Profile: {}\x07".format(profile))
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'simulate': False,
            'format': 'best',
            'outtmpl': 'soundcloud/{}/%(webpage_url_basename)s/%(title)s.%(id)s.%(ext)s'.format(profile),
            'continuedl': True,
            'writeinfojson': True,
            'restrictfilenames': False,
            'nooverwrites': True,
            'embed_thumbnail': True,
            'nocheckcertificate': False,
            'prefer_insecure': False,
            'socket_timeout': '600',
            'retries': 10,
            #'external_downloader': 'axel',
            #'external_downloader_args': ['--num-connections=16'],
            'logger': ydl_logger(),
            'progress_hooks': [ydl_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info('https://soundcloud.com/{}'.format(profile))
