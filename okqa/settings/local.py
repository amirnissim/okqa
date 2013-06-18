from __future__ import absolute_import
import os

from .base import *

STATIC_S3 = False

ENV = 'LOCAL'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'devdb',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'postgres',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bennydaon@gmail.com'
EMAIL_HOST_PASSWORD = 'Atari1200XL'

LOGGING['handlers']['console']['level'] = 'DEBUG'

if not STATIC_S3:
    STATIC_URL = '/static/'
    STATIC_PATH = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200',
        'INDEX_NAME': 'qa',
    },
}
