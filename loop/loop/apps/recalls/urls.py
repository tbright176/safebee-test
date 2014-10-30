from django.conf.urls import patterns, url

from .views import (ProductRecallDetailView, ProductRecallHomePageView,
                    ProductRecallSearchView)


urlpatterns = patterns('',
                       url(r'detail/(?P<pk>\d+)/$',
                           ProductRecallDetailView.as_view(),
                           name="recalls_detail"),
    url(r'search/$', ProductRecallSearchView.as_view(), name="recalls_search"),
    url(r'^', ProductRecallHomePageView.as_view(), name="recalls_home"),
)
