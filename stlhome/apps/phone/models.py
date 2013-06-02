from django.db import models

class Call(models.Model):
    'call from Twilio'
    sid = models.CharField(max_length=34)
    bed_count = models.PositiveIntegerField()
