#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
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
    #url(r'^faritra/$', views.get_faritra, name='faritra'),
)

# Titre du site et de diverses sections
admin.site.site_header = 'Administration' # Text to put in each page's <h1>.
admin.site.site_title = 'Atlas CNLS' # Text to put at the end of each page's <title>.
admin.site.index_title = 'Gestion des actions de lutte contre le SIDA' # Text to put at the top of the admin index page.
admin.site.site_url = None # Remove the "View on site" link from the admin change view
