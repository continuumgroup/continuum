from django.db import models

from stlhome.apps.shelters.models import Shelter

class Call(models.Model):
    'call from Twilio'
    sid = models.CharField(max_length=34)
    bed_count = models.PositiveIntegerField(default=0)
    shelter = models.ForeignKey(Shelter, null=True)
