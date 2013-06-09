from os import environ
from django.conf import settings
from twilio.rest import TwilioRestClient

class Client(TwilioClient):
    '''client wrapper around TwilioClient'''
    def __init__(self):
        super(TwilioClient, self).__init__(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

client = Client()
