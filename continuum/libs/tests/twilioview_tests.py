'tests for continuum.libs.tests.twilioview'
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
