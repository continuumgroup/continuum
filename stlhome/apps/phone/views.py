from twilio.twiml import Response
from django_twilio.decorators import twilio_view

from stlhome.lib.twilioview import TwilioView

class HelloWorldView(TwilioView):
    def get(self, request):
        r = Response()
        r.say('Hello, World')
        return r
