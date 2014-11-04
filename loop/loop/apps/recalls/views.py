from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView

from recalls.models import ProductRecall, CarRecall, FoodRecall, RecallStreamItem


class BaseRecallView(object):
    context_object_name = 'recall'


class RecallDetailView(BaseRecallView, DetailView):
    template_name = "recalls/recall_detail.html"


class RecallHomePageView(BaseRecallView, TemplateView):
    template_name = "recalls/home.html"

    def get_context_data(self, **kwargs):
        context = super(RecallHomePageView, self).get_context_data(**kwargs)
        return context


class RecallListView(BaseRecallView, ListView):
    template_name = "recalls/recall_search.html"
    model = RecallStreamItem
    paginate_by = 15
    page_kwarg = "page_num"

    def get_context_data(self, **kwargs):
        context = super(RecallListView, self).get_context_data(**kwargs)

        list_title_map = {
            RecallStreamItem: 'All Recalls',
            ProductRecall: 'Product Recalls',
            FoodRecall: 'Food & Drug Recalls',
            CarRecall: 'Vehicle Recalls'
        }

        context['category_title'] = list_title_map[self.model]

        return context


class CarRecallDetailView(RecallDetailView):
    model = CarRecall


class ProductRecallDetailView(RecallDetailView):
    model = ProductRecall


class FoodRecallDetailView(RecallDetailView):
    model = FoodRecall


class RecallSearchView(RecallListView):
    pass
