from django.shortcuts import render

from loop.core.views import ContentDetailView

from .models import Feature


class FeatureDetailView(ContentDetailView):
    model = Feature
    template_name = 'feature_landing.html'
    queryset = Feature.published.all()
