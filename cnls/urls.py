#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^geoactions/$', views.get_geoactions, name='geoactions'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    #url(r'^faritra/$', views.get_faritra, name='faritra'),
)
