#!/usr/bin/env python
import urllib2
import json
import time
import errno
import os
import sys
import logging
import redis
import pickle
from bs4 import BeautifulSoup as bs
from timeout import timeout
from datetime import datetime

__author__ = 'An'

LOG_FILE = 'dotaonly.log'
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE, mode='w')
log.addHandler(handler)

TIME_OUT = 10
INTERVAL = 240
EXPCEPTION_INTERVAL = 2

def getHtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    return page


@timeout(TIME_OUT, os.strerror(errno.ETIMEDOUT))
def getTopStreamDouyu():
    arr = []
    dic = {}

    base_url = 'http://www.douyutv.com'
    dire_url = base_url+'/directory/game/DOTA2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('div', attrs={'id': 'item_data'}).findAll('li'):
        stream_title = li.a['title']
        stream_link = li.a['href']
        stream_img = li.find('img')['data-original']
        stream_anchor = li.find('span', attrs={'class': 'nnt'}).string

        stream_id = stream_img.split('/')[-1].split('_')[0]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor,
                      'title': stream_title, 'img': stream_img,
                      'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


@timeout(TIME_OUT, os.strerror(errno.ETIMEDOUT))
def getTopStreamZhanqi():
    arr = []
    dic = {}

    base_url = 'http://www.zhanqi.tv'
    dire_url = base_url+'/games/dota2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('ul', attrs={'id': 'hotList'}).findAll('li'):
        stream_title = li.find('span', attrs={'class': 'name'}).string
        stream_link = li.find('a', attrs={'class': 'js-jump-link'})['href']
        stream_img = li.find('img')['src']
        stream_anchor = li.find('span', attrs={'class': 'anchor'}).string
        stream_id = li['data-room-id']

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor,
                      'title': stream_title, 'img': stream_img,
                      'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


@timeout(TIME_OUT, os.strerror(errno.ETIMEDOUT))
def getTopStreamHuomao():
    arr = []
    dic = {}

    base_url = 'http://www.huomaotv.com'
    dire_url = base_url+'/live_list?gid=23'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.findAll('div', attrs={'class': 'VOD'}):
        stream_title = li.find('dl',
                               attrs={'class': 'VOD_title'}).dt.a['title']
        stream_link = li.find('a', attrs={'class': 'play_btn'})['href']
        stream_img = base_url+li.find('img')['data-src']
        stream_anchor = li.find('a', attrs={'class': 'LiveAuthor'}).string
        stream_id = stream_link.split('/')[-1]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor,
                      'title': stream_title,
                      'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


@timeout(TIME_OUT, os.strerror(errno.ETIMEDOUT))
def getTopStreamHuya():
    arr = []
    dic = {}

    base_url = 'http://www.huya.com'
    dire_url = base_url+'/g/dota2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    theScript = ""

    for s in dire_soup.findAll('script'):
        if s.string is not None and 'videoList = [' in s.string:
            theScript = s.string
            break
    jsonValue = '[%s]' % (theScript.split('[', 1)[1].rsplit(']', 1)[0],)

    json_object = json.loads(jsonValue)

    for stream in json_object:
        stream_id = stream['channel'] + '/' + stream['liveChannel']
        stream_anchor = stream['nick'].strip()
        stream_title = stream['roomName'].strip()
        stream_link = stream['privateHost']
        stream_img = stream['screenshot']

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor,
                      'title': stream_title, 'img': stream_img,
                      'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


@timeout(TIME_OUT, os.strerror(errno.ETIMEDOUT))
def getTopStreamTwitch():
    arr = []
    dic = {}

    url = 'https://api.twitch.tv/kraken/streams?game=dota%202'
    js = json.load(urllib2.urlopen(url))

    streams = js['streams']

    for stream in streams:
        stream_img = stream['preview']['medium']  # stream_img
        stream_title = stream['channel']['status']  # stream_title
        stream_anchor = stream['channel']['display_name']  # stream_anchor
        stream_link = stream['channel']['name']  # stream_link
        stream_id = stream['channel']['url']  # stream_id

        #  0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor,
                      'title': stream_title,
                      'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


def saveToJsonFile(redis_client):

    log.debug("Stream json refreshing...")
    try:
        start = time.time()
        data = getTopStreamDouyu()
        redis_client.set(':1:douyu', pickle.dumps(json.dumps(data)))
        log.debug("Douyu Time consume: %d" % (time.time()-start))
    except Exception as e:
        log.debug("Douyu Error")
        log.debug(e.message)
        return False

    try:
        start = time.time()
        data = getTopStreamZhanqi()
        redis_client.set(':1:zhanqi', pickle.dumps(json.dumps(data)))
        log.debug("Zhanqi Time consume: %d" % (time.time()-start))
    except Exception as e:
        log.debug("Zhanqi Error")
        log.debug(e.message)
        return False

    try:
        start = time.time()
        data = getTopStreamHuomao()
        redis_client.set(':1:huomao', pickle.dumps(json.dumps(data)))
        log.debug("Huomao Time consume: %d" % (time.time()-start))
    except Exception as e:
        log.debug("Huomao Error")
        log.debug(e.message)
        return False

    try:
        start = time.time()
        data = getTopStreamHuya()
        redis_client.set(':1:huya', pickle.dumps(json.dumps(data)))
        log.debug("Huya Time consume: %d" % (time.time()-start))
    except Exception as e:
        log.debug("Huya Error")
        log.debug(e.message)
        return False

    try:
        start = time.time()
        data = getTopStreamTwitch()
        redis_client.set(':1:twitch', pickle.dumps(json.dumps(data)))
        log.debug("Twitch Time consume: %d" % (time.time()-start))
    except Exception as e:
        log.debug("Twitch Error")
        log.debug(e.message)
        return False

    return True


def main():
    redis_client = redis.StrictRedis()
    while True:
        log.debug('alive...')
        sleep_time = INTERVAL
        try:
            start = time.time()
            if not saveToJsonFile(redis_client):
                sleep_time = EXPCEPTION_INTERVAL
        except:
            log.debug("error occurs, passing the error")
            sleep_time = EXPCEPTION_INTERVAL
        time.sleep(sleep_time)


def daemonize():
    pid = os.fork()
    if pid > 0:
        os.wait()
        sys.exit(0)

    os.setsid()
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    main()


if __name__ == '__main__':
    daemonize()
