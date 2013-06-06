from os import environ
from django.conf import settings
from twilio.rest import TwilioRestClient

if 'CI' in environ:  # mock things out to test anyway, please
    from mock import Mock
    client = Mock()
else:
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
