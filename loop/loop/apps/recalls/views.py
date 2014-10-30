from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from recalls.models import ProductRecall


class ProductRecallHomePageView(TemplateView):
    template_name = "recalls/home.html"


class ProductRecallDetailView(DetailView):
    template_name = "recalls/recall_detail.html"

    context_object_name = 'recall'
    model = ProductRecall
    queryset = ProductRecall.objects.all()


class ProductRecallSearchView(TemplateView):
    template_name = "recalls/recall_search.html"
