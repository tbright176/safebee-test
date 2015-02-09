from django.conf.urls import patterns, url

from .views import BuzzViewAll


urlpatterns = patterns('',
    url(r'^$', BuzzViewAll.as_view(), name='buzz_view_all'),
)
