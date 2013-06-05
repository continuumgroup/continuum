from stlhome.lib.test import BaseTest
from ..models import ClientCall


class ClientCallTests(BaseTest):
    '''tests for ClientCall object'''
    def verb_classes(self, resp):
        return [type(verb) for verb in resp.verbs]

    def assertFromTo(self, source, method_name, target, *args, **kwargs):
        cc = self.deliver(ClientCall, call_state=source)
        getattr(cc, method_name)(*args, **kwargs)

        self.assertEqual(target, cc.call_state)

        return cc

    def test_transfer_to_operator_from_welcome(self):
        'transfer_to_operator available from welcome'
        self.assertFromTo('welcome', 'transfer_to_operator', 'operator')

    def test_transfer_to_operator_from_other(self):
        'transfer_to_operator available from anywhere'
        self.assertFromTo('does_not_exist_1234', 'transfer_to_operator', 'operator')

    def test_request_location(self):
        'request_location available from welcome'
        self.assertFromTo('welcome', 'request_location', 'requested_location')

    def test_process_location(self):
        '''process_location pulls relevant data out of view and uses it'''
        cc = self.assertFromTo(
            'requested_location', 'process_location', 'processed_location', 
            request=self.factory.post('/', {'RecordingUrl': 'test'}),
        )
        self.assertEqual('test', cc.location_name)
