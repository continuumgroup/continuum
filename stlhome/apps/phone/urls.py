from django.conf.urls.defaults import patterns, include, url

from .views import HelloWorldView

urlpatterns = patterns(
    '',
    url(r'^hello_world/$', HelloWorldView.as_view(), name='hello_world'),
)
