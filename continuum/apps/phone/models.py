from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django_fsm.db.fields import FSMField, transition
from twilio.twiml import Response
from urlparse import urljoin

from continuum.apps.shelters.models import Shelter
from continuum.lib.twilioclient import client

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

    # states from which more data can be collected
    COLLECT_DATA_STATES = [
        'welcome',
        'processed_location',
        'processed_name',
        'processed_bed_count',
    ]

    @transition(source='*', target='operator', save=True)
    def transfer_to_operator(self):
        '''transfer/connect to an operator, this class does not concern itself with further steps'''

    @transition(source='*', target='enqueued', save=True)
    def enqueue(self):
        '''"enqueue" this call (put on hold)'''

    @transition(source='enqueued', target='dequeued', save=True)
    def dequeue(self, url, method='GET'):
        '''"dequeue" this call (take off hold)'''
        site = Site.objects.get_current()
        client.calls.route(
            sid=self.sid,
            method=method,
            url=urljoin('http://' + site.domain, url)
        )

    @transition(source='dequeued', target='confirmed', save=True)
    def confirm(self):
        '''confirm shelter placement'''

    @transition(source='*', target='declined', save=True)
    def decline(self):
        '''decline shelter placement (no match found/rejection)'''

    @transition(source=COLLECT_DATA_STATES, target='requested_location', save=True)
    def request_location(self):
        '''request client location, via voice'''

    @transition(source='requested_location', target='processed_location', save=True)
    def process_location(self, request):
        '''process location from a given request'''
        # TODO: fill stub with appropriate GIS conversion
        self.location_name = request.POST.get('RecordingUrl', '')

    @transition(source=COLLECT_DATA_STATES, target='requested_name', save=True)
    def request_name(self):
        '''request client name, via voice'''

    @transition(source='requested_name', target='processed_name', save=True)
    def process_name(self, request):
        '''process name from a given request'''
        self.client_name = request.POST.get('RecordingUrl', '')

    @transition(source=COLLECT_DATA_STATES, target='requested_bed_count', save=True)
    def request_bed_count(self):
        '''request number of beds required'''

    @transition(source='requested_bed_count', target='processed_bed_count', save=True)
    def process_bed_count(self, request):
        '''process beds from a given request'''
        self.bed_count = int(request.POST['Digits'])
