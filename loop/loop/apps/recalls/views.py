from django.shortcuts import render
from django.views.generic import TemplateView


class ProductRecallHomePageView(TemplateView):
    template_name = "recalls/home.html"


class ProductRecallDetailView(TemplateView):
    template_name = "recalls/recall_detail.html"


class ProductRecallSearchView(TemplateView):
    template_name = "recalls/recall_search.html"
