from django.views.generic import View
from django.http import HttpResponse

class TwilioView(View):
    '''return a twillio XML response'''
    def dispatch(self, *args, **kwargs):
        'dispatch based on verb'
        twilio_resp = super(TwilioView, self).dispatch(*args, **kwargs)
        return HttpResponse(
            unicode(twilio_resp),
            mimetype='application/xml',
        )
