'''testing settings'''
import sys
if 'test' in sys.argv:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
