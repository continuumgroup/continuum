'tests for geocoding'
from continuum.libs.test import BaseTest
from django.conf import settings
import httpretty

from ..geocoding import address_to_latlng, GeoCodingError, NoResultsError, BadDataError

class AddressToLatlngTests(BaseTest):
    @httpretty.activate
    def test_raises_zero_results(self):
        'if no results are found, raises a NoResultsError'
        httpretty.register_uri(
            httpretty.GET, settings.GEOCODING_API_ENDPOINT,
            body='{"results" : [], "status" : "ZERO_RESULTS"}',
            content_type='application/json'
        )

        self.assertRaisesRegexp(
            NoResultsError, 'No results for ""',
            address_to_latlng, ''
        )

    @httpretty.activate
    def test_raises_bad_data_error(self):
        'if bad data is passed, raises a BadDataError'
        httpretty.register_uri(
            httpretty.GET, settings.GEOCODING_API_ENDPOINT,
            body='{"results" : [], "status" : "SOMETHING"}',
            content_type='application/json'
        )

        self.assertRaises(BadDataError, address_to_latlng, '')
