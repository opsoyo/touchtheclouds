#!/usr/bin/python3

from __future__ import unicode_literals
import time
import json
import youtube_dl
import sys

class ydl_logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def ydl_hook(d):
    if d['status'] == 'finished':
        print('\r\n*****\r\nYTDL>> Download complete...{}\r\n*****'.format(d['filename']))

with open('profiles.json') as data_file:
    data = json.load(data_file)

    for char in data:
        for profile in data[char]:
            #print('Working profile: {}'.format(profile))
            sys.stdout.write("\x1b]2;Working Profile: {}\x07".format(profile))
            ydl_opts = {
                #'consoletitle': 'Working Profile: %(uploader)s',
                'quiet': False,
                'no_warnings': False,
                'ignoreerrors': False,
                'verbose': False,
                'simulate': False,
                'continuedl': True,
                'restrictfilenames': True,
                'nooverwrites': True,
                'format': 'best',
                'outtmpl': 'soundcloud/%(uploader)s/%(webpage_url_basename)s/%(title)s.%(id)s/%(title)s.%(id)s.%(ext)s',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                'writeinfojson': True,
                'writedescription': True,
                'write_all_thumbnails': True,
                'nocheckcertificate': False,
                'prefer_insecure': False,
                'socket_timeout': '600',
                'retries': 10,
                #'debug_printtraffic': True,
                #'dump_pages': True,
                #'call_home': True,
                'external_downloader': 'aria2c',
                'external_downloader_args': ['-c','-j','3','-x','3','-s','3','-k','1M'],
                'logger': ydl_logger(),
                'progress_hooks': [ydl_hook],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                results = ydl.download(['https://soundcloud.com/{}'.format(profile)])
