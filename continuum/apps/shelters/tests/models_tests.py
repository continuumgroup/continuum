'test shelters models'
from continuum.libs.test import BaseTest
from mock import patch

from ..models import Shelter

class ShelterModelTests(BaseTest):
    @patch('apps.shelters.models.address_to_latlng')
    def test_set_coords_uses_address_to_latlng(self, m_atl):
        'set_coords uses address_to_latlng'
        m_atl.return_value = (90, -90)

        x = Shelter(address='127 Main Street, 63134')
        x.set_coords()

        m_atl.assert_called_with(x.address)
        self.assertEqual(m_atl.return_value[0], x.latitude)
        self.assertEqual(m_atl.return_value[1], x.longitude)

    @patch('apps.shelters.models.address_to_latlng')
    def test_set_coords_on_save(self, m_atl):
        'set_coords is called on save'
        m_atl.return_value = (90, -90)

        x = Shelter(address='127 Main Street, 63134')
        x.save()

        m_atl.assert_called_with(x.address)
        self.assertEqual(m_atl.return_value[0], x.latitude)
        self.assertEqual(m_atl.return_value[1], x.longitude)
