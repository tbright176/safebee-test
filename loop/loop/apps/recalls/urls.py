from django.conf.urls import patterns, url

from .models import CarRecall, ProductRecall, FoodRecall
from .views import (RecallHomePageView, RecallSearchView, RecallListView,
                    RecallDetailView, RecallSignUpView)


urlpatterns = patterns('',
    url(r'cars/(?P<pk>\d+)/$', RecallDetailView.as_view(model=CarRecall), name="car_recall_detail"),
    url(r'food/(?P<pk>\d+)/$', RecallDetailView.as_view(model=FoodRecall), name="food_recall_detail"),
    url(r'products/(?P<pk>\d+)/$', RecallDetailView.as_view(model=ProductRecall), name="product_recall_detail"),
    url(r'products(?:/page/(?P<page_num>\d+))?', RecallListView.as_view(model=ProductRecall), name="product_recall_list"),
    url(r'cars(?:/page/(?P<page_num>\d+))?', RecallListView.as_view(model=CarRecall), name="car_recall_list"),
    url(r'food(?:/page/(?P<page_num>\d+))?', RecallListView.as_view(model=FoodRecall), name="food_recall_list"),
    url(r'all(?:/page/(?P<page_num>\d+))?', RecallListView.as_view(), name="recalls_list"),
    url(r'search/', RecallSearchView.as_view(), name="recalls_search"),
    url(r'sign-up/', RecallSignUpView.as_view(), name="recalls_signup"),
    url(r'^', RecallHomePageView.as_view(), name="recalls_home"),
)
