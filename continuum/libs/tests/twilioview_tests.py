'tests for continuum.libs.tests.twilioview'
from ..test import BaseTest
from ..twilioview import TwilioView

class TwilioViewTests(BaseTest):
    'tests for TwilioView'
    def setUp(self):
        self.view = TwilioView.as_view()

    def test_no_signature(self):
        'no signature is forbidden'
        req = self.factory.post('/')
        self.assertEqual(405, self.view(req).status_code)
