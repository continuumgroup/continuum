from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django_fsm.db.fields import FSMField, transition
from twilio.twiml import Response

from stlhome.apps.shelters.models import Shelter

class ClientCall(models.Model):
    'call from Twilio'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sid = models.CharField(max_length=34, db_index=True)
    bed_count = models.PositiveIntegerField(default=0)
    shelter = models.ForeignKey(Shelter, null=True)

    location_name = models.CharField(max_length=300, null=True, blank=True)
    client_name = models.CharField(max_length=300, null=True, blank=True)

    call_state = FSMField(default='welcome')

    @transition(source='*', target='operator', save=True)
    def transfer_to_operator(self):
        '''transfer/connect to an operator, this class does not concern itself with further steps'''

    @transition(source='welcome', target='requested_location', save=True)
    def request_location(self):
        '''request client location, via voice'''

    @transition(source='requested_location', target='processed_location', save=True)
    def process_location(self, request):
        '''process location from a given request'''
        self.location_name = request.POST.get('RecordingUrl', '')
