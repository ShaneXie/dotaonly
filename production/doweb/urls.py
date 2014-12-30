from django.conf.urls import patterns, include, url
from django.contrib import admin
from dotalive import views as live_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',live_views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^live/$',live_views.live_index),
    url(r'^live/(\d{5})/$',live_views.live_index_bysite),
    url(r'^live/ajax/getStreamList/(\d{3})/$',live_views.loadStreamList),
)
