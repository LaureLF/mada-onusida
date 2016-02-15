# mada-onusida

Pour configurer la connexion à la base de données, vous aurez besoin de créer un fichier perso.py dans le même répertoire que settings.py, et d'y écrire le code suivant :

```python
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
```
