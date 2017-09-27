#!/usr/bin/python3

from __future__ import unicode_literals
import time
import json
import youtube_dl
import sys
import socket

def is_connected(host="8.8.8.8", port=53):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as ex:
            pass
        return False

class ydl_logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        if 'ssl' in msg:
            # Network error, check for Internet in loop
            while True:
                is_conn = is_connected('https://google.com')
                if is_conn == True:
                    break
                else:
                    epoch = int(time.time())
                    print("\r\n*****\r\nNetwork Error ({}): No Internet. Waiting to recheck.\r\n*****\r\n".format(epoch))
                    print('Error result: {}'.format(is_conn))
                    time.sleep(2)
        elif 'No space left on device':
            print('\r\n*****\r\nYeah??: {}\r\n*****'.format(msg))
        elif '404' in msg:
            pass
        else:
            print(msg)

def ydl_hook(d):
    if d['status'] == 'finished':
        print('\r\n*****\r\nYTDL>> Download complete...{}\r\n*****'.format(d['filename']))

"""
Search for .aria2c temp files to complete
and reprocess that user in attempt to finish.
Remove temp file if not possible
"""
# ...

# Read from JSON and find a random profile
with open('profiles.json') as data_file:
    data = json.load(data_file)

for char in data:
    for profile in data[char]:
        profile = 'quarion'
        print('Working profile: {}'.format(profile))
        #sys.stdout.write("\x1b]2;Working Profile: {}\x07".format(profile))
        ydl_opts = {
            #'consoletitle': 'Working Profile: %(uploader)s',
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True, # So that it doesn't stop on random 404s
            'verbose': False,
            'simulate': False,
            'continuedl': True,
            'restrictfilenames': True,
            'nooverwrites': True,
            'format': 'all',
            'outtmpl': 'soundcloud/{}/%(uploader)s/%(webpage_url_basename)s/%(title)s.%(id)s/%(title)s.%(id)s.%(ext)s'.format(profile), # Designed to account for artist name's changing with the same username, and the same for the songs by using the IDs as part of the dirs and filenames.
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
            'download_archive': 'downloaded.log',
            'external_downloader': 'aria2c',
            'external_downloader_args': ['-c','-j','3','-x','3','-s','3','-k','1M','--max-tries','10'],
            'logger': ydl_logger(),
            'progress_hooks': [ydl_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            results = ydl.download(['https://soundcloud.com/{}/tracks'.format(profile)])
