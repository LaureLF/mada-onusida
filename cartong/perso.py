# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/ #databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '$$$', # Name of your spatial database
        'USER': '$$$', # Database user
        'PASSWORD': '$$$', # Database password 
        'HOST': '195.154.35.191',
        'PORT':'5432',
    }
}

# A adapter selon les installations
GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'
