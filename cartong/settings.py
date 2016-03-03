# -*- coding: utf-8 -*-

"""
Django settings for cartong project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Import personnal database and path config
from .perso import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a--2c!c3m)t21o1ght4jn(&q#ad-(88bhzljr$mx0%4*lw)44e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
##    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'cnls',
    'leaflet',
##    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cartong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
##                'django.template.context_processors.i18n',
##                'django.template.context_processors.media',
##                'django.template.context_processors.static',
##                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

WSGI_APPLICATION = 'cartong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Déplacé dans perso.py en prévision de la migration vers un dépôt ouvert


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Leaflet config for admin site
# https://github.com/makinacorpus/django-leaflet

LEAFLET_CONFIG = {
#    'SPATIAL_EXTENT': (42.0, -26.0, 52.0, -11.0),
    'DEFAULT_CENTER': (49.0, -18.5),
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 5,
    'MAX_ZOOM': 18,
    'TILES': [('OpenStreetMap', 'http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {'attribution': "Tiles courtesy of <a href='http://www.mapquest.com/'>MapQuest</a>, &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='http://www.opendatacommons.org/licenses/odbl'>ODbL</a>"})],
    'RESET_VIEW': False,
#    'MINIMAP': True # constructeur non reconnu
}