from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'stlhome.apps.phone.views',
    url(r'^hello_world/$', 'hello_world', name='hello_world'),
)
