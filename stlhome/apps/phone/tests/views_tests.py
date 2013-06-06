from django.core.urlresolvers import reverse
from mock import patch

from stlhome.lib.test import BaseTest

from .. import views
from ..models import ClientCall


class TwilioTest(BaseTest):
    '''test case for Twilio views'''
    def setUp(self):
        self.sid = 'sid'
        self.cc = self.deliver(ClientCall, sid=self.sid, call_state='welcome')

    def tearDown(self):
        '''clean up objects created during test'''
        self.addCleanup(ClientCall.objects.filter(sid=self.sid).delete)

    def request(self, method, data=None):
        all_data = {'CallSid': self.sid}

        data = data or {}
        all_data.update(data)

        factory_method = getattr(self.factory, method)
        view_method = getattr(self.view, method)
        return view_method(factory_method('/', all_data))

    def get(self, data=None):
        return self.request('get', data)

    def post(self, data=None):
        return self.request('post', data)


class StartViewTests(TwilioTest):
    '''test for StartView'''
    view = views.StartView()

    def test_get_creates_client_call(self):
        '''GET creates a ClientCall object (with a given CallSid)'''
        ClientCall.objects.filter(sid=self.sid).delete()
        self.get()
        self.assertEqual(1, ClientCall.objects.filter(sid=self.sid).count())

    def test_gather_redirects(self):
        '''GET eventually redirects to phone:start with POST'''
        resp = self.get()

        _, gather = resp.verbs
        self.assertEqual('POST', gather.attrs['method'])
        self.assertEqual(reverse('phone:start'), gather.attrs['action'])

    def test_post_1(self):
        '''a 1 digit redirects to collect_location'''
        resp = self.post({'Digits': '1'})
        self.assertEqual(
            reverse('phone:collect_location'),
            resp['location']
        )

    def test_post_0(self):
        '''a 0 digit redirects to operator'''
        resp = self.post({'Digits': '0'})
        self.assertEqual(
            reverse('phone:operator'),
            resp['location']
        )

    def test_post_any(self):
        '''any digit but 1 or 0 redirects to start'''
        resp = self.post({'Digits': '2'})
        self.assertEqual(
            reverse('phone:start'),
            resp['location']
        )
