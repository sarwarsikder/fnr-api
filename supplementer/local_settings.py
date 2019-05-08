### if copied and renamed to local_settings.py this file will override productions settings for local development
### local_settings.py
### environment-specific settings
### example with a development environment
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG


os.environ['ENVIRONMENT_TYPE'] = 'development'

# DATABASES = {
#     'default': {
#         'NAME': 'supplementer_db',
#         'ENGINE': 'django.db.backends.mysql',
#         'USER': 'root',
#         'PASSWORD': 'Wsit_97480',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'autocommit': True,
#         },
#     }
# }
# API_URL = 'http://192.168.1.10:8000/api'
# API_CLIENT_ID = "zMLYnt4lYTAXwe6CTfUVGLG9pbikgqzUbsnWGNx0"
# API_CLIENT_SECRET = "qo95nkxrF9GjACj1TyDHz8V6Apkx994xYGbguaZcK3E8zzSox5Z7k8J0DYBxlGnAVGvfFwmoDbJkVCFh0VZEHdEaxvbYuJM7A0n8npV8W79ZmPbYWCep8Und8UCm9TI2"
# API_GRANT_TYPE = "password"
DATABASES = {
    'default': {
        'NAME': 'supplementer_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '1',
        'HOST': 'supplementer_db',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

LOCAL_ENV = True

SITE_URL = 'http://127.0.0.1:8000'

