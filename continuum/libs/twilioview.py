from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from twilio.twiml import Response
from twilio.util import RequestValidator

class TwilioView(View):
    '''return a twillio XML response'''
    def verify_request(self):
        'verify request comes from Twilio'
        # this bit taken from Randal Degges' django-twilio library, which as of
        # 1c020e2a7c6f4845e7309d7277380c8b76d38ba4 has been released into the
        # public domain
        try:
            validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            url = self.request.build_absolute_uri()
            signature = self.request.META['HTTP_X_TWILIO_SIGNATURE']
        except (AttributeError, KeyError):
            return HttpResponseForbidden()

        if not validator.validate(url, request.POST, signature):
            return HttpResponseForbidden()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        'dispatch based on verb'
        if not settings.DEBUG:
            self.verify_request()

        twilio_resp = super(TwilioView, self).dispatch(*args, **kwargs)

        if isinstance(twilio_resp, Response):
            return HttpResponse(
                twilio_resp.toxml(xml_declaration=True),
                mimetype='application/xml',
            )
        else:
            return twilio_resp
