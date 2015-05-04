from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
import django
import os
import json


# Create your views here.
pwd = os.path.dirname(__file__)

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def live_index(request):
    page = {
        'title': 'Test Page',
        'content': django.get_version()
    }

    return render_to_response('live_index.html',{'page': page}, context_instance=RequestContext(request))

def live_index_bysite(request,source_site):
    page = {
        'title': source_site,
        'content': django.get_version()
    }

    return render_to_response('live_base.html',{'page': page}, context_instance=RequestContext(request))


def get_cache():
    pass


def loadStreamList(request,site_code):
    # site_code
    # 001 = douyu 002=Zhanqi 003=Huomao 004= huya 005 = twitch
    type=""
    if int(site_code) == 001:
        streamList = json.loads(cache.get('douyu'))
        type='Douyu'
    if int(site_code) == 002:
        streamList = json.loads(cache.get('zhanqi'))
        type='Zhanqi'
    if int(site_code) == 003:
        streamList = json.loads(cache.get('huomao'))
        type='Huomao'
    if int(site_code) == 004:
        streamList = json.loads(cache.get('huya'))
        type='Huya'
    if int(site_code) == 005:
        streamList = json.loads(cache.get('twitch'))
        type='Twitch'

    return render_to_response('list_ajax.html',{'streamList': streamList, 'type':type}, context_instance=RequestContext(request))