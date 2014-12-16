#!/usr/bin/env python
# encoding: utf-8
import sys
#sys.path.append('/usr/local/lib/python3.7/site-packages')                                                    

import praw
import time
import pprint
import os
import requests
from PIL import Image
from StringIO import StringIO
from StringIO import StringIO

DESKTOP_DIR = '/Users/ataylor/Pictures/desktop/'

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
    sys.exit(0)
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
print time.ctime(), 'changed to ', title
