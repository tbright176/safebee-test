from django.conf.urls import patterns, url

from .views import (ProductRecallDetailView, ProductRecallHomePageView)


urlpatterns = patterns('',
    url(r'detail/$', ProductRecallDetailView.as_view(), name="recalls_detail"),
    url(r'^', ProductRecallHomePageView.as_view(), name="recalls_home"),
)
