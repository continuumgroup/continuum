from django.conf.urls.defaults import patterns, include, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^start/$', StartView.as_view(), name='start'),
    url(r'^operator/$', OperatorView.as_view(), name='operator'),
    url(r'^collect_location/$', CollectLocationView.as_view(), name='collect_location'),
    url(r'^bed_count/$', BedCountView.as_view(), name='bed_count'),
    url(r'^find_shelter/$', FindShelterView.as_view(), name='find_shelter'),
    url(r'^start_shelter_call/$', ShelterCallView.as_view(), name='start_shelter_call'),
)
