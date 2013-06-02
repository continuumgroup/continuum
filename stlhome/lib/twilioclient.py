from django.conf import settings
from twilio.rest import TwilioRestClient

client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
