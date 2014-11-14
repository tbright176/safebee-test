from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView, ListView

from watson.views import SearchMixin

from recalls.models import (ProductRecall, CarRecall, FoodRecall,
                            RecallStreamItem)


class BaseRecallView(object):
    context_object_name = 'recall'


class RecallDetailView(BaseRecallView, DetailView):
    template_name = "recalls/recall_detail.html"
    model = RecallStreamItem

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs.get('slug', None),
                                 recall_number=self.kwargs.get('recall_number', None))

    def get_context_data(self, **kwargs):
        context = super(RecallDetailView, self).get_context_data(**kwargs)

        section_header_map = {
            ProductRecall: 'Consumer Products',
            FoodRecall: 'Food & Drug',
            CarRecall: 'Motor Vehicle'
        }
        context['section_header_text'] = section_header_map[self.model]
        context['page_header_text'] = "Product Recalls"

        recall_category_map = {
            ProductRecall: 'product_recall_list',
            FoodRecall: 'food_recall_list',
            CarRecall: 'car_recall_list',
        }
        context['recall_category_url'] = recall_category_map[self.model]
        return context


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
    list_title = 'Latest Results'

    def get_list_title(self):
        return self.list_title

    def get_context_data(self, **kwargs):
        context = super(RecallListView, self).get_context_data(**kwargs)

        list_title_map = {
            RecallStreamItem: 'All Recalls',
            ProductRecall: 'Product Recalls',
            FoodRecall: 'Food & Drug Recalls',
            CarRecall: 'Vehicle Recalls'
        }

        context['category_title'] = list_title_map[self.model]
        context['list_title'] = self.get_list_title()
        return context

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the paginator for this view.
        """
        per_page = per_page
        if self.request.GET.get('page_size'):
            per_page = self.request.GET.get('page_size')
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_queryset(self):
        """
        Modify sort based on url param 'sort'. Possible values include
        'latest' and 'oldest'.

        'latest' is the default
        """
        queryset = super(RecallListView, self).get_queryset()
        sort = self.request.GET.get('sort')

        if sort:
            queryset = queryset.order_by('recall_date')

        return queryset

    def dispatch(self, request, *args, **kwargs):
        try:
            handler = super(RecallListView, self).dispatch(request, *args, **kwargs)
        except Http404:
            if self.page_kwarg in kwargs:
                kwargs.pop(self.page_kwarg)
                self.kwargs.pop(self.page_kwarg)
                handler = super(RecallListView, self).dispatch(request, *args, **kwargs)

        return handler


class RecallSearchView(SearchMixin, RecallListView):
    template_name = "recalls/recall_search.html"

    def get_list_title(self):
        query = self.request.GET.get('q')
        if self.object_list:
            return '"{}" Results'.format(query)
        elif query:
            return '"{}" Returned 0 Results.'.format(query)

        return super(RecallSearchView, self).get_list_title()

    def get_context_data(self, **kwargs):
        context = super(RecallSearchView, self).get_context_data(**kwargs)
        context['category_title'] = 'Search Results'
        return context


class RecallSignUpView(TemplateView):
    template_name = "recalls/subscribe.html"
