import json

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView, ListView, FormView

from boto.exception import BotoServerError
from boto.sns import connect_to_region

from watson.views import SearchMixin

from recalls.forms import RecallSignUpForm
from recalls.models import (ProductRecall, CarRecall, FoodRecall,
                            RecallStreamItem, RecallSNSTopic, CarMake, CarModel)


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
            ProductRecall: 'Consumer Products',
            FoodRecall: 'Food & Drugs',
            CarRecall: 'Motor Vehicles'
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


class RecallSignUpSuccessView(TemplateView):
    template_name = "recalls/recall_signup_success.html"


class RecallSignUpView(FormView):
    template_name = "recalls/subscribe.html"
    form_class = RecallSignUpForm
    success_url = reverse_lazy('recalls_signup')

    def form_valid(self, form):
        """
        Determine the endpoint and topic.

        1. Create the topic if it does not exist
        2. subscribe the endpoint to the topic
        """
        data = form.cleaned_data
        # required for SNS subscription
        subscription_reqs = []

        # get subscription method
        if data['phone_number']:
            subscription_reqs.append({
                'endpoint': data['phone_number'],
                'protocol': 'sms'
            })

        if data['email']:
            subscription_reqs.append({
                'endpoint': data['email'],
                'protocol': 'email'
            })

        conn = connect_to_region(
            'us-east-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        for topic in form.get_topics():
            try:
                topic_result = RecallSNSTopic.objects.get(name=topic['topic'])
            except RecallSNSTopic.DoesNotExist:
                api_resp = conn.create_topic(topic)
                try:
                    arn = api_resp['CreateTopicResponse']['CreateTopicResult']['TopicArn']
                    display_resp = conn.set_topic_attributes(arn, 'DisplayName', topic['display'])
                except KeyError:
                    messages.error(self.request, 'Uh oh! There was a problem creating the subscription!')
                finally:
                    topic_result = RecallSNSTopic.objects.create(
                        name=topic['topic'],
                        arn=arn
                    )

            for req in subscription_reqs:
                try:
                    conn.subscribe(topic_result.arn, req['protocol'], req['endpoint'])
                    messages.success(self.request, 'Subscription created for {}'.format(req['endpoint']))
                except BotoServerError:
                    messages.error(self.request, 'Error creating subscription for {}'.format(req['endpoint']))

        return super(RecallSignUpView, self).form_valid(form)

def car_models(request):
    ret = []
    make = CarMake.objects.get(pk=request.GET.get('make_id'))
    if make:
        for model in make.carmodel_set.all():
            ret.append(dict(id=model.id, value=model.name))
    if len(ret)!=1:
        ret.insert(0, dict(id='', value=''))

    return HttpResponse(json.dumps(ret),
                        content_type='application/json')

def car_years(request):
    ret = []
    model_id = request.GET.get('model_id')
    if model_id and model_id != 'null':
        model = CarModel.objects.get(pk=model_id)
        ret = [dict(id=year, value=year) for year in model.years.split(',')]
        ret.sort(reverse=True)
    return HttpResponse(json.dumps(ret),
                        content_type='application/json')
