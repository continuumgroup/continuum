from django.conf.urls.defaults import patterns, include, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^start/$', StartView.as_view(), name='start'),
    url(r'^operator/$', OperatorView.as_view(), name='operator'),
    url(r'^collect_location/$', CollectLocationView.as_view(), name='collect_location'),
    url(r'^bed_count/$', BedCountView.as_view(), name='bed_count'),
    url(r'^find_shelter/$', FindShelterView.as_view(), name='find_shelter'),
    url(r'^start_shelter_call/(?P<client_call>\d+)/(?P<pks>.+)/$', ShelterCallView.as_view(), name='start_shelter_call'),
    url(r'^shelter_call_callback/(?P<client_call>\d+)/(?P<pks>.*)/$', shelter_call_callback, name='shelter_call_callback'),
    url(r'^post_shelter_call/(?P<client_call>\d+)/(?P<pks>.*)/$', PostShelterCallView.as_view(), name='post_shelter_call'),
    url(r'^verify_shelter_availability/(?P<client_call>\d+)/(?P<pk>\d+)/$', VerifyShelterAvailabilityView.as_view(), name='verify_shelter_availability'),
)
