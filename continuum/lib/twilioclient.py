from os import environ
from django.conf import settings
from twilio.rest import TwilioRestClient

class Client(TwilioRestClient):
    '''client wrapper around TwilioRestClient'''
    def __init__(self):
        super(Client, self).__init__(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

client = Client()
