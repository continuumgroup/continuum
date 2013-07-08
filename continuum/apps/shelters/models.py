from datetime import datetime
from django.conf import settings
from django.db import models
import logging
# from pygeocoder import Geocoder

from continuum.libs.choice import Choice

logger = logging.getLogger(__name__)

class ClassifierChoices(Choice):
    ALLOW = 'allow'
    BLOCK = 'block'


class ShelterManager(models.Manager):
    '''manage and query shelter objects'''
    def available(self):
        '''available shelters (defined as those with available beds)'''
        return self.get_queryset().exclude(
            availability__when=datetime.now() - settings.AVAILABILITY_EXPIRY,
            availability__available=0
        )


class Shelter(models.Model):
    '''a single location shelter'''
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12)
    classifier_action = models.CharField(
        max_length=ClassifierChoices.longest_length(),
        choices=ClassifierChoices, default=ClassifierChoices.BLOCK
    )

    # location
    address = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True)

    objects = ShelterManager()

    def set_coords(self):
        '''set coordinates based on an address'''
        self.latitude, self.longitude = 0, 0
        # result = Geocoder.geocode(self.address)
        # # use the first result, if you can't, log and exit
        # try:
        #     location = result.data[0]['geometry']['location']
        # except IndexError:
        #     logger.exception('Error geocoding')
        #     return
        # except KeyError:
        #     logger.exception('Misformated Geocoder data')
        #     return

        # self.latitude, self.longitude = location['lat'], location['lng']

    @classmethod
    def pre_save(cls, **kwargs):
        'hook into a pre_save signal, registered elsewhere'
        instance = kwargs['instance']
        if not instance.latitude or not instance.longitude:
            instance.set_coords()

# connect singals for Shelter
models.signals.pre_save.connect(Shelter.pre_save, sender=Shelter)


class Availability(models.Model):
    '''record how many beds are available at a checkpoint'''
    shelter = models.ForeignKey(Shelter)

    when = models.DateTimeField(auto_now_add=True)
    available = models.PositiveIntegerField()
