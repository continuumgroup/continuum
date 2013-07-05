'geocoding'
from django.conf import settings
from urllib import urlencode

import requests

def address_to_latlng(address):
    'convert a textual address to a lat, long pair'
    geocoded_address = requests.get('%s?%s' % (
        settings.GEOCODING_API_ENDPOINT,
        urlencode({
            'sensor': 'false',
            'address': address
        })
    ))
    try:
        coords = geocoded_address.json()['results'][0]['geometry']['location']
    except (KeyError, IndexError):
        raise ValueError('No data: "%s"' % address)

    return coords['lat'], coords['lng']
