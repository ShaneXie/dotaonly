__author__ = 'An'
import urllib2
import json
from bs4 import BeautifulSoup as bs

def getHtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    return page

def getTopStreamDouyu():
    retArr = []

    base_url = 'http://www.douyutv.com'
    dire_url = base_url+'/directory/game/DOTA2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('div', attrs={'id':'item_data'}).findAll('li')[:10]:
        stream_title = li.a['title']
        stream_link = li.a['href']
        stream_img = li.find('img')['data-original']
        stream_anchor = li.find('span',attrs={'class':'nnt'}).string

        stream_id = stream_img.split('/')[-1].split('_')[0]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamTuple= stream_id,stream_anchor,stream_title,stream_img,stream_link
        retArr.append(streamTuple)

        #print stream_title + " " + stream_link + " " + stream_id
        #print stream_img
        #print stream_anchor+"\n"

    return retArr

def getTopStreamZhanqi():
    retArr = []

    base_url = 'http://www.zhanqi.tv'
    dire_url = base_url+'/games/dota2'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.find('ul', attrs={'id':'hotList'}).findAll('li')[:10]:
        stream_title = li.find('a',attrs={'class':'name'}).string
        stream_link = li.find('a',attrs={'class':'name'})['href']
        stream_img = li.find('img')['src']
        stream_anchor = li.find('a',attrs={'class':'anchor'}).string
        stream_id = li['data-room-id']

        # 0=id 1=anchor 2=title 3=img 4=link
        streamTuple= stream_id,stream_anchor,stream_title,stream_img,stream_link
        retArr.append(streamTuple)

        #print stream_title + " " + stream_link + " " + stream_id
        #print stream_img
        #print stream_anchor+"\n"

    return retArr

def getTopStreamHuomao():
    retArr = []

    base_url = 'http://www.huomaotv.com'
    dire_url = base_url+'/live_list?gid=23'

    dire_page = getHtml(dire_url)
    dire_soup = bs(dire_page)

    for li in dire_soup.findAll('div', attrs={'class':'VOD'})[:10]:
        stream_title = li.find('dl',attrs={'class':'VOD_title'}).dt.a['title']
        stream_link = li.find('a',attrs={'class':'play_btn'})['href']
        stream_img = base_url+li.find('img')['data-src']
        stream_anchor = li.find('a',attrs={'class':'LiveAuthor'}).string
        stream_id = stream_link.split('/')[-1]

        # 0=id 1=anchor 2=title 3=img 4=link
        streamTuple= stream_id,stream_anchor,stream_title,stream_img,stream_link
        retArr.append(streamTuple)

        #print stream_title + " " + stream_link + " " + stream_id
        #print stream_img
        #print stream_anchor+"\n"

    return retArr


def getTopStreamHuya():
    retArr = []

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

    for stream in json_object[:6]:
        stream_id = stream['channel'] +'/'+stream['liveChannel']
        stream_anchor = stream['nick'].strip()
        stream_title = stream['roomName'].strip()
        stream_link = stream['privateHost']
        stream_img = "http://assets.dwstatic.com/amkit/p/duya/common/img/default_live.jpg"

        # 0=id 1=anchor 2=title 3=img 4=link
        streamTuple= stream_id,stream_anchor,stream_title,stream_img,stream_link
        retArr.append(streamTuple)

    return retArr


def getTopStreamTwitch():
    retArr = []

    url = 'https://api.twitch.tv/kraken/search/streams?q="Dota%202"'
    js = json.load(urllib2.urlopen(url))

    streams = js['streams']

    for stream in streams[:10]:
        stream_img = stream['preview']['medium'] #stream_img
        stream_title = stream['channel']['status'] #stream_title
        stream_anchor = stream['channel']['display_name'] #stream_anchor
        stream_link = stream['channel']['name'] #stream_link
        stream_id = stream['channel']['url'] #stream_id

        # 0=id 1=anchor 2=title 3=img 4=link
        streamTuple= stream_id,stream_anchor,stream_title,stream_img,stream_link
        retArr.append(streamTuple)

        #print stream_title + " " + stream_link + " " + stream_id
        #print stream_img
        #print stream_anchor+"\n"

    return retArr


if __name__ == '__main__':
    arr = getTopStreamTwitch()
    for s in arr:
        print ("%s  %s  %s  %s  %s")%(s[0],s[1],s[2],s[3],s[4])
else:
    print 'imported by others'
