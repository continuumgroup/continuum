from django.conf.urls.defaults import patterns, include, url

from .views import *

urlpatterns = patterns(
    '',
    url(r'^start/$', StartView.as_view(), name='start'),
    url(r'^collect_location/$', CollectLocationView.as_view(), name='collect_location'),
)
