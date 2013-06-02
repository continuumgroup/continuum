from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'django_twilio.views',
    url(r'^hello_world/$', 'say', {
        'text': 'Hello, world!',
    }),
)
