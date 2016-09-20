#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from feedback import views

urlpatterns = patterns('',
    # Le formulaire de remontée de bugs
    url(r'^bugs\/?$', views.submit_bug, name='bugs'),
    url(r'^bugs\/merci\/?$', views.merci, name='merci'),
)

