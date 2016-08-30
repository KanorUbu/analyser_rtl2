#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import sys
from bs4 import BeautifulSoup
from datetime import datetime, time


def parsedate_str2obj(time_str):
    return datetime.strptime(time_str, "%d/%m/%Y %H:%M")


def parsedate_unicode2str(time_unicode):
    time_str = time_unicode.encode('utf8')
    return datetime.strptime(time_str[:19],
        "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")

"""
http://www.rtl2.fr/quel-est-ce-titre?date=22%2F08%2F2016&hour=20&minute=31
"""
if not sys.argv[1]:
    print("ERREUR : pas d'arguments")
    sys.exit(0)
start_date_time = sys.argv[1]

#start_date_time = '26/08/2016'

#d = datetime.strptime(start_date_time, "%d/%m/%Y")
#t = time(start_hour, start_minute)
#last_date_time = datetime.combine(d, t)
last_date_time = datetime.combine(
    datetime.strptime(start_date_time, "%d/%m/%Y"),
    time(23, 59)
    )

filedata = open(last_date_time.strftime("%d%m%Y") + ".txt", 'w')
filedata.write('timestamp;artist;title\n')

while last_date_time.day == int(start_date_time[:2]):
    # Construct the URL
    params = urllib.urlencode(
        {'date': last_date_time.strftime("%d/%m/%Y"),
        'hour': last_date_time.hour,
        'minute': last_date_time.minute}
        )

    urlbase = "http://www.rtl2.fr/quel-est-ce-titre"

    f = urllib.urlopen(urlbase, params)

    # Parse the HTML webpage
    parsed_html = BeautifulSoup(f, "html.parser")

    # Copy informations about the songs
    timestamps = parsed_html.findAll("time")
    titles = parsed_html.find_all("h2", "song-title")
    artists = parsed_html.find_all("p", "song-artist")

    # Ouptut the results
    if len(timestamps) == len(titles) and len(artists) == len(timestamps):
        l = len(timestamps)
        for i in range(l):
            ti = parsedate_unicode2str(timestamps[i]['datetime'])
            a = artists[i].string
            t = titles[i].string
            print('%s ==> %s : %s' % (ti, a, t))
            last_date_time = parsedate_str2obj(ti)
            if int(ti[:2]) == int(start_date_time[:2]):
                data = ti + ';' + a + ';' + t + '\n'
                filedata.write(data.encode('utf-8'))
filedata.close()
