import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': dj_database_url.config(default='sqlite:///./okqa.db')}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
