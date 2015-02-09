from django.conf.urls import patterns, url

from .views import FeatureDetailView


urlpatterns = patterns('',
    url(r'^(?P<category_slug>[-,\+\w]+)(?:/(?P<sub_category_slug>[-,\+\w]+))?/(?P<basename>[-,\+\w]+)$',
        FeatureDetailView.as_view(), name='features_feature'),
)
