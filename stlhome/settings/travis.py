"""Production settings and globals."""


from os import environ

from memcacheify import memcacheify
from postgresify import postgresify

from common import *


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = postgresify()
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = memcacheify()
########## END CACHE CONFIGURATION
