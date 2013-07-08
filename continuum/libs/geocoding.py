'geocoding'
from django.conf import settings
import sys
from urllib import urlencode

import requests


class GeoCodingError(Exception):
    pass


class NoResultsError(GeoCodingError):
    pass


class BadDataError(GeoCodingError):
    pass


def address_to_latlng(address):
    'convert a textual address to a lat, long pair'
    geocoded_address = requests.get('%s?%s' % (
        settings.GEOCODING_API_ENDPOINT,
        urlencode({
            'sensor': 'false',
            'address': address
        })
    ))
    jsonified = geocoded_address.json()

    if jsonified.get('status') == 'ZERO_RESULTS':
        raise NoResultsError('No results for "%s"' % address)

    try:
        coords = geocoded_address.json()['results'][0]['geometry']['location']
    except (KeyError, IndexError) as err:
        raise BadDataError(str(err)), None, sys.exc_info()[2]

    return coords['lat'], coords['lng']
