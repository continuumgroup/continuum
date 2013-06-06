from django.core.urlresolvers import reverse
from mock import patch, Mock

from stlhome.lib.test import BaseTest

from .. import views
from ..models import ClientCall


class TwilioTest(BaseTest):
    '''test case for Twilio views'''
    def setUp(self):
        self.sid = 'sid'
        self.cc = self.deliver(ClientCall, sid=self.sid, call_state='welcome')
        self.addCleanup(ClientCall.objects.filter(sid=self.sid).delete)

    def assertState(self, state):
        '''assert a state of the given call, given a state'''
        # reference isn't updated, so fetch fresh
        self.assertEqual(state, ClientCall.objects.get(sid=self.sid).call_state)

    def set_state(self, state):
        '''update ClientCall with new state'''
        self.cc.call_state = state
        self.cc.save()

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


class CollectLocationViewTests(TwilioTest):
    '''tests for CollectLocationView'''
    view = views.CollectLocationView()
    def test_get_records(self):
        '''records location (audio)'''
        r = self.get()
        
        _, record = r.verbs
        self.assertEqual('POST', record.attrs['method'])
        self.assertEqual(reverse('phone:collect_location'), record.attrs['action'])

    def test_get_calls_request_location(self):
        '''calls request_location on a ClientCall GET'''
        self.get()

    def test_post_redirects(self):
        '''POST redirects to bed_count'''
        self.set_state('requested_location')
        resp = self.post({'RecordingUrl': 'test'})

        self.assertEqual(
            reverse('phone:collect_name'),
            resp['location']
        )

    def test_post_calls_process_location(self):
        '''calls process_location on a ClientCall POST'''
        self.set_state('requested_location')
        self.post({'RecordingUrl': 'test'})

        self.assertState('processed_location')


class CollectNameViewTests(TwilioTest):
    '''tests for CollectNameView'''
    view = views.CollectNameView()
    def test_get_records(self):
        '''GET records audio'''
        resp = self.get()

        _, record = resp.verbs
        self.assertEqual('POST', record.attrs['method'])
        self.assertEqual(reverse('phone:collect_name'), record.attrs['action'])

    def test_get_calls_request_name(self):
        '''GET calls request_name on ClientCall'''
        self.get()
        self.assertState('requested_name')

    def test_post_redirects(self):
        '''POST redirects'''
        self.set_state('requested_name')
        resp = self.post({'RecordingUrl': 'test'})

        self.assertEqual(
            reverse('phone:bed_count'),
            resp['location']
        )

    def test_post_calls_process_name(self):
        '''POST calls process_name on ClientCall'''
        self.set_state('requested_name')
        self.post({'RecordingUrl': 'test'})
        self.assertState('processed_name')
