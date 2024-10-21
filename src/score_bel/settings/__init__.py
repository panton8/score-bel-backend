import os
import sys

import environ

from .apps import *
from .auth_user import *
from .databases import *
from .middlewares import *
from .templates import *
from .rest_framework import *
from .drf_spectacular import *

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.abspath(os.path.join(__file__, '../../../'))

sys.path.append(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='w7rgREGGRW78te4RG#7e4g$rg45EW')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

ROOT_URLCONF = 'score_bel.urls'

WSGI_APPLICATION = 'score_bel.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '../', 'static')
STATIC_URL = 'staticfiles/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGIN_REGEXES = env.list('CORS_ALLOWED_ORIGIN_REGEXES',
                                       default=['http://localhost:3000'])

APPEND_SLASH = env.bool('APPEND_SLASH', default=True)
