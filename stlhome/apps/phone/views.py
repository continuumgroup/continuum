from twilio.twiml import Response
from django_twilio.decorators import twilio_view

@twilio_view
def hello_world(request):
    r = Response()
    r.say('Hello, World')
    return r
