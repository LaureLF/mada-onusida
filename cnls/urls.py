#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from cnls import views

urlpatterns = patterns('',
    # La carte (écran d'accueil)
    url(r'^$', views.home, name='home'),
    # Une page affichant le GeoJson format texte (utilisé seulement à des fins de test)
    url(r'^geoactions\/?$', views.get_geoactions, name='geoactions'),
    # Le fichier robots.txt à destination des "web crawlers"
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
#    url(r'(?i)^(?P<action_echelle>[a-zA-Z]+)\/(?P<action_id>[0-9]+)/$', views.detail, name='detail'),
    # L'onglet À propos
    url(r'^a_propos\/?$', views.apropos, name='apropos'),
    # Le chargement du fichier CSV d'export
    url(r'^actions$', views.export_csv, name='export_csv'),
    # La vue détaillée de l'action choisir
    url(r'^(?P<classe>[a-zA-Z]+)\/(?P<id>\d+)\/.*$', views.detail, name='detail'),
    #favicons
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/media/favicons/favicon.ico', permanent=True)),
    url(r'^android-chrome-192x192\.png$', RedirectView.as_view(url='/static/media/favicons/android-chrome-192x192.png', permanent=True)),
    url(r'^browserconfig\.xml$', RedirectView.as_view(url='/static/media/favicons/browserconfig.xml', permanent=True)),
    url(r'^mstile-150x150\.png$', RedirectView.as_view(url='/static/media/favicons/mstile-150x150.png', permanent=True)),
    # Inusité
    #url(r'^faritra/$', views.get_faritra, name='faritra'),
)
