from app.settings.base import *

DEBUG = True

SECRET_KEY = 'notasecretdevkey'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_ROOT = BASE_DIR / 'static/media'