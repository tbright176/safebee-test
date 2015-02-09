from django.conf.urls import patterns

urlpatterns = patterns('loop.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
