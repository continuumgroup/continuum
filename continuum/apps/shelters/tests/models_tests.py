'''tests for continuum.apps.shelters.models'''
from decimal import Decimal
from continuum.lib.test import BaseTest

from continuum.apps.shelters.models import Shelter


class GeoQueryMixinTests(BaseTest):
    shelter_lat, shelter_long = Decimal('38.6698499'), Decimal('-90.257488')

    def test_very_close(self):
        shelter = self.deliver(
            Shelter,
            latitude=self.shelter_lat, longitude=self.shelter_long
        )
        self.assertItemsEqual(
            [shelter],
            Shelter.objects.near(self.shelter_lat, self.shelter_long, 100)
        )

    def test_a_mile_away(self):
        shelter = self.deliver(
            Shelter,
            latitude=self.shelter_lat, longitude=self.shelter_long
        )

        delta = Decimal('0.01')
        lat, lng = self.shelter_lat - delta, self.shelter_long - delta
        mile_in_meters = 1609.34

        self.assertItemsEqual(
            [shelter],
            Shelter.objects.near(lat, lng, mile_in_meters)
        )

    def test_over_a_mile(self):
        shelter = self.deliver(
            Shelter,
            latitude=self.shelter_lat, longitude=self.shelter_long
        )

        delta = Decimal('0.02')
        lat, lng = self.shelter_lat - delta, self.shelter_long - delta
        mile_in_meters = 1609.34

        self.assertItemsEqual(
            [],
            Shelter.objects.near(lat, lng, mile_in_meters)
        )
