from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from recalls.mixins import LatestAndPopularMixin
from recalls.models import ProductRecall



class ProductRecallHomePageView(LatestAndPopularMixin, TemplateView):
    template_name = "recalls/home.html"

    def get_context_data(self, **kwargs):
        context = super(ProductRecallHomePageView, self).get_context_data(**kwargs)
        return context


class ProductRecallDetailView(LatestAndPopularMixin, DetailView):
    template_name = "recalls/recall_detail.html"

    context_object_name = 'recall'
    model = ProductRecall
    queryset = ProductRecall.objects.all()


class ProductRecallSearchView(TemplateView):
    template_name = "recalls/recall_search.html"
