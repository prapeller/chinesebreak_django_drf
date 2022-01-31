from app.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['mysite.com']
SECRET_KEY = 'supertopsecretproductionkey'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'NAME': 'chinesebreak_db',
        'PASSWORD': 'secretpass',
        'HOST': 'db',
        'PORT': '5432'
    }
}

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static/'