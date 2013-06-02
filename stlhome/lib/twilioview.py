from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from twilio.twiml import Response

class TwilioView(View):
    '''return a twillio XML response'''
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        'dispatch based on verb'
        twilio_resp = super(TwilioView, self).dispatch(*args, **kwargs)
        if isinstance(twilio_resp, Response):
            return HttpResponse(
                twilio_resp.toxml(xml_declaration=True),
                mimetype='application/xml',
            )
        else:
            return twilio_resp