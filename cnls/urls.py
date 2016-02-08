
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
#    url(r'^actions/$', views.get_actions, name='actions'),
#    url(r'^actions/title/(?P<title>[\w\ ]+)$', views.get_actions_by_title),
    url(r'^geoactions/$', views.get_geoactions, name='geoactions'),

    #url(r'^faritra/$', views.get_faritra, name='faritra'),
)
