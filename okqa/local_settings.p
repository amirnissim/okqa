import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default': dj_database_url.config(default='sqlite:///./okqa.db')}
