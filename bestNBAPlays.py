# -*- coding: utf-8 -*-
import re
import time
import urllib2
import json
import twitter

api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

regex_top_string = '(Top (10|5) NBA (Assists|Dunks|Plays|Blocks))|((Assists|Dunks|Plays|Blocks) of the Week)'
regex_top = re.compile(regex_top_string, re.IGNORECASE)

url = 'http://gdata.youtube.com/feeds/api/users/nba/uploads?v=2&alt=json&q=%22top%22&order‌​by=published&max-results=3'
last_entry = None
while True:

    response = urllib2.urlopen(url).read().decode('utf-8')
    data = json.loads(response)
    data_feed_entry = data['feed']['entry']
    first_entry = None

    for entries in data_feed_entry:
        if not first_entry:
            first_entry = entries['id']['$t']
        if last_entry == entries['id']['$t']:
            break
        result = regex_top.search(entries['title']['$t'])
        if result:
            video_title = entries['title']['$t']
            video_link = 'youtu.be/' + entries['media$group']['yt$videoid']['$t']
            try:
                status = api.PostUpdate(video_title + ' ' + video_link + ' #NBA')
            except Exception as e:
                print('Error', e)
                exit(1)

    last_entry = first_entry
    time.sleep(1800)
