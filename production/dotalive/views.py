from django.shortcuts import render_to_response
from django.template import RequestContext
import django
import liveData as ld

# Create your views here.

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

def loadStreamList(request,site_code):
    # site_code
    # 001 = douyu 002=Zhanqi 003=Huomao 004= huya 005 = twitch
    type=""
    if int(site_code) == 001:
        streamList = ld.getTopStreamDouyu()
        type='Douyu'
    if int(site_code) == 002:
        streamList = ld.getTopStreamZhanqi()
        type='Zhanqi'
    if int(site_code) == 003:
        streamList = ld.getTopStreamHuomao()
        type='Huomao'
    if int(site_code) == 004:
        streamList = ld.getTopStreamHuya()
        type='Huya'
    if int(site_code) == 005:
        streamList = ld.getTopStreamTwitch()
        type='Twitch'

    return render_to_response('list_ajax.html',{'streamList': streamList, 'type':type}, context_instance=RequestContext(request))