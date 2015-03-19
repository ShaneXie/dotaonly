__author__ = 'An'
import urllib2
import json
import time
import os
import sys
from bs4 import BeautifulSoup as bs


def getHtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    return page


def getTopStreamDouyu():
    arr = []
    dic = {}

    base_url = 'http://www.douyutv.com'
    dire_url = base_url+'/directory/game/DOTA2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('div', attrs={'id':'item_data'}).findAll('li'):
        stream_title = li.a['title']
        stream_link = li.a['href']
        stream_img = li.find('img')['data-original']
        stream_anchor = li.find('span',attrs={'class':'nnt'}).string

        stream_id = stream_img.split('/')[-1].split('_')[0]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor, 'title': stream_title, 'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic

def getTopStreamZhanqi():
    arr = []
    dic = {}

    base_url = 'http://www.zhanqi.tv'
    dire_url = base_url+'/games/dota2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('ul', attrs={'id':'hotList'}).findAll('li'):
        stream_title = li.find('a',attrs={'class':'name'}).string
        stream_link = li.find('a',attrs={'class':'name'})['href']
        stream_img = li.find('img')['src']
        stream_anchor = li.find('a',attrs={'class':'anchor'}).string
        stream_id = li['data-room-id']

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor, 'title': stream_title, 'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


def getTopStreamHuomao():
    arr = []
    dic ={}

    base_url = 'http://www.huomaotv.com'
    dire_url = base_url+'/live_list?gid=23'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.findAll('div', attrs={'class':'VOD'}):
        stream_title = li.find('dl',attrs={'class':'VOD_title'}).dt.a['title']
        stream_link = li.find('a',attrs={'class':'play_btn'})['href']
        stream_img = base_url+li.find('img')['data-src']
        stream_anchor = li.find('a',attrs={'class':'LiveAuthor'}).string
        stream_id = stream_link.split('/')[-1]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor, 'title': stream_title, 'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


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
        stream_id = stream['channel'] +'/'+stream['liveChannel']
        stream_anchor = stream['nick'].strip()
        stream_title = stream['roomName'].strip()
        stream_link = stream['privateHost']
        stream_img = stream['screenshot']

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor, 'title': stream_title, 'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


def getTopStreamTwitch():
    arr = []
    dic = {}

    url = 'https://api.twitch.tv/kraken/streams?game=dota%202'
    js = json.load(urllib2.urlopen(url))

    streams = js['streams']

    for stream in streams:
        stream_img = stream['preview']['medium'] #stream_img
        stream_title = stream['channel']['status'] #stream_title
        stream_anchor = stream['channel']['display_name'] #stream_anchor
        stream_link = stream['channel']['name'] #stream_link
        stream_id = stream['channel']['url'] #stream_id

        # 0=id 1=anchor 2=title 3=img 4=link
        streamDict = {'id': stream_id, 'anchor': stream_anchor, 'title': stream_title, 'img': stream_img, 'link': stream_link}
        arr.append(streamDict)

    dic['streams'] = arr
    return dic


def saveToJsonFile():

    with open('json/douyu.json', 'w') as outJson:
        json.dump(getTopStreamDouyu(), outJson)

    with open('json/zhanqi.json', 'w') as outJson:
        json.dump(getTopStreamZhanqi(), outJson)

    with open('json/huomao.json', 'w') as outJson:
        json.dump(getTopStreamHuomao(), outJson)

    with open('json/huya.json', 'w') as outJson:
        json.dump(getTopStreamHuya(), outJson)

    with open('json/twitch.json', 'w') as outJson:
        json.dump(getTopStreamTwitch(), outJson)

    return True


def main():
    counter = 1
    while True:
        try:
            saveToJsonFile()
        except:
            print "error occurs, passing the error"
            pass
        print "Json has been saved to file_%d"%counter
        counter += 1
        time.sleep(15)


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
else:
    print 'imported by others'
