from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView

from recalls.mixins import LatestRecallsMixin
from recalls.models import ProductRecall, CarRecall, FoodRecall, RecallStreamItem


class BaseRecallView(LatestRecallsMixin):
    context_object_name = 'recall'


class RecallDetailView(BaseRecallView, DetailView):
    template_name = "recalls/recall_detail.html"


class RecallHomePageView(BaseRecallView, TemplateView):
    template_name = "recalls/home.html"

    def get_context_data(self, **kwargs):
        context = super(ProductRecallHomePageView, self).get_context_data(**kwargs)
        return context


class RecallListView(BaseRecallView, ListView):
    template_name = "recalls/recall_search.html"
    queryset = RecallStreamItem.objects.all()


class CarRecallDetailView(RecallDetailView):
    model = CarRecall


class ProductRecallDetailView(RecallDetailView):
    model = ProductRecall


class FoodRecallDetailView(RecallDetailView):
    model = FoodRecall


class RecallSearchView(RecallListView):
    pass
