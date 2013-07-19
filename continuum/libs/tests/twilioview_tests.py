'tests for continuum.libs.tests.twilioview'
from django.conf import settings
from django.core.exceptions import PermissionDenied
from twilio.util import RequestValidator

from ..test import BaseTest
from ..twilioview import TwilioView

class TwilioViewTests(BaseTest):
    'tests for TwilioView'
    def setUp(self):
        self.view = TwilioView()

    def test_no_signature(self):
        'no signature is forbidden'
        self.view.request = self.factory.post('/', data={'a': 'b'})

        self.assertRaises(PermissionDenied, self.view.verify_request)

    def test_bad_signature(self):
        'bad signature is forbidden'
        self.view.request = self.factory.post('/', data={'a': 'b'})
        self.view.request.META['HTTP_X_TWILIO_SIGNATURE'] = 'bad_signature'

        self.assertRaises(PermissionDenied, self.view.verify_request)

    def test_good_signature(self):
        'good signature is allowed'
        with self.settings(TWILIO_AUTH_TOKEN='fred'):
            req = self.factory.post('/', data={'a': 'b'})

            validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            req.META['HTTP_X_TWILIO_SIGNATURE'] = validator.compute_signature(
                req.build_absolute_uri(), req.POST
            )

            self.view.request = req

            try:
                self.view.verify_request()
            except PermissionDenied:
                self.fail('Raised PermissionDenied when not expecting it')

    def test_good_signature_GET(self):
        'good signature is allowed on GET'
        with self.settings(TWILIO_AUTH_TOKEN='fred'):
            req = self.factory.get('/', data={'a': 'b'})

            validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            req.META['HTTP_X_TWILIO_SIGNATURE'] = validator.compute_signature(
                req.build_absolute_uri(), req.POST
            )

            self.view.request = req

            try:
                self.view.verify_request()
            except PermissionDenied:
                self.fail('Raised PermissionDenied when not expecting it')
