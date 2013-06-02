from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from twilio.twiml import Response
from django_twilio.decorators import twilio_view

from stlhome.lib.twilioview import TwilioView

class StartView(TwilioView):
    def get(self, request):
        r = Response()

        r.say('''You have reached the St. Louis homeless help hotline. If you need immediate help, hang up and dial 9 1 1.''')
        with r.gather(finishOnKey='#', method='POST', action=reverse('phone:start'), numDigits=1) as g:
            g.say('If you need a bed tonight, press 1. To speak with a volunteer, press 0.')

        return r

    def post(self, request):
        if request.POST['Digits'] == '1':
            return redirect(reverse('phone:collect_location'))
        elif request.POST['Digits'] == '0':
            r = Response()
            r.say('You are calling an operator now in your mind')
        else:
            r = redirect(reverse('phone:start'))

        return r

class CollectLocationView(TwilioView):
    def get(self, request):
        r = Response()
        
        r.say('''"Where are you now? At the tone, please say an address or street intersection in the Saint Louis area. Then press Pound.''')
        r.record(action=reverse('phone:collect_location'), method='POST', maxLength=10, timeout=2, transcribe=True)

        return r

    def post(self, request):
        print request.POST

        r = Response()
        r.say('thanks. love ya')
        return r
