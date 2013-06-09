from mock import patch

from stlhome.lib.test import BaseTest
from ..models import ClientCall


class ClientCallTests(BaseTest):
    '''tests for ClientCall object'''
    def verb_classes(self, resp):
        return [type(verb) for verb in resp.verbs]

    def assertTransition(self, source, method_name, target, *args, **kwargs):
        cc = self.deliver(ClientCall, call_state=source)
        getattr(cc, method_name)(*args, **kwargs)

        self.assertEqual(target, cc.call_state)

        return cc

    def test_transfer_to_operator_from_welcome(self):
        '''transfer_to_operator available from welcome'''
        self.assertTransition('welcome', 'transfer_to_operator', 'operator')

    def test_transfer_to_operator_from_other(self):
        '''transfer_to_operator available from anywhere'''
        self.assertTransition('does_not_exist_1234', 'transfer_to_operator', 'operator')

    def test_request_location(self):
        '''request_location available from COLLECT_DATA_STATES'''
        for state in ClientCall.COLLECT_DATA_STATES:
            self.assertTransition(state, 'request_location', 'requested_location')

    def test_process_location(self):
        '''process_location pulls relevant data out of a request and uses it'''
        cc = self.assertTransition(
            'requested_location', 'process_location', 'processed_location', 
            request=self.factory.post('/', {'RecordingUrl': 'test'}),
        )
        self.assertEqual('test', cc.location_name)

    def test_request_name(self):
        '''request_name available from COLLECT_DATA_STATES'''
        for state in ClientCall.COLLECT_DATA_STATES:
            self.assertTransition(state, 'request_name', 'requested_name')

    def test_process_name(self):
        '''process_name pulls relevant data out of a request and uses it'''
        cc = self.assertTransition(
            'requested_name', 'process_name', 'processed_name',
            request=self.factory.post('/', {'RecordingUrl': 'test'}),
        )
        self.assertEqual('test', cc.client_name)

    def test_request_bed_count(self):
        '''request_bed_count available from COLLECT_DATA_STATES'''
        for state in ClientCall.COLLECT_DATA_STATES:
            self.assertTransition(state, 'request_bed_count', 'requested_bed_count')

    def test_process_bed_count(self):
        '''request_bed_count pulls relevant data out of a request and uses it'''
        cc = self.assertTransition(
            'requested_bed_count', 'process_bed_count', 'processed_bed_count',
            request=self.factory.post('/', {'Digits': '2'})
        )

        self.assertEqual(2, cc.bed_count)

    def test_enqueue(self):
        '''enqueue from anywhere'''
        self.assertTransition('welcome', 'enqueue', 'enqueued')

    def test_confirm(self):
        '''confirm from dequeued'''
        self.assertTransition('dequeued', 'confirm', 'confirmed')

    def test_decline(self):
        '''decline from anywhere'''
        self.assertTransition('welcome', 'decline', 'declined')

    # TODO: get this test working again
    # @patch('stlhome.apps.phone.models.client')
    # def test_dequeued(self, mock_client):
    #     cc = self.assertTransition(
    #         'enqueued', 'dequeue', 'dequeued',
    #         url='test', method='TEST'
    #     )

    #     mock_client.calls.route.assert_called_with(
    #         sid=cc.sid,
    #         method='TEST',
    #         url='http://example.com/test',
    #     )
