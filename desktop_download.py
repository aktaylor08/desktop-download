#!/usr/bin/env python
# encoding: utf-8
import sys

import subprocess

import praw
import time
import os
import requests
from PIL import Image
from StringIO import StringIO

DESKTOP_DIR = '/home/ataylor/Pictures/desktop/'

#get the current info file if it exists
info_file = DESKTOP_DIR + '.current'
if os.path.isfile(info_file):
    current = open(info_file, 'r').readline().strip()
else:
    current = None

#get the submissions from reddit
r = praw.Reddit('Earthporn desktop downloader take two by gonebraska')
sub = r.get_subreddit('earthporn')
submissions = sub.get_hot(limit=15)
for i in submissions:
    link = i.url
    title = i.title
    sub_id = i.id
    #check to see if the link ends with .jpg or it is on imgur to get 
    # a good link to used
    if link.endswith('.jpg'):
        link = link
        break
    elif 'imgur' in link:
        link = link + '.jpg'
        break
    else:
        continue

    #if the top usable post is what we are already using break
if i.id == current:
    print("Already there")
    #sys.exit(-1)
else:
    #remove the old one
    if current is not None:
        if os.path.isfile( DESKTOP_DIR + current + '.jpg'):
            os.remove(DESKTOP_DIR + current + '.jpg')
        
#save the image
req = requests.get(link)
image = Image.open(StringIO(req.content))
loc = DESKTOP_DIR + sub_id + '.jpg'
image.save(loc,  "JPEG")

#write out the current
open(DESKTOP_DIR + '.current', 'w').write(i.id)
pid = subprocess.check_output(["pgrep", "gnome-session"])
pid = pid.lstrip().rstrip()
dbus_address = subprocess.check_output(["grep", "-z", "DBUS_SESSION_BUS_ADDRESS", "/proc/{:s}/environ".format(pid), ])#"|", "-d=" ])
dbus_address = '='.join(dbus_address.split('=')[1:])
dbus_address = dbus_address.encode('string-escape')

os.environ["DBUS_SESSION_BUS_ADDRESS"] = dbus_address.lstrip().strip()



out = subprocess.check_output(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://{:s}".format(loc)])
print time.ctime(), 'changed to ', title
