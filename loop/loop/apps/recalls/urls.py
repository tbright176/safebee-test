from django.conf.urls import patterns, url

from .models import CarRecall, ProductRecall, FoodRecall
from .views import (RecallHomePageView, RecallSearchView, RecallListView,
                    CarRecallDetailView, FoodRecallDetailView, ProductRecallDetailView)


urlpatterns = patterns('',
    url(r'cars/(?P<pk>\d+)/$', CarRecallDetailView.as_view(), name="car_recall_detail"),
    url(r'food/(?P<pk>\d+)/$', FoodRecallDetailView.as_view(), name="food_recall_detail"),
    url(r'products/(?P<pk>\d+)/$', ProductRecallDetailView.as_view(), name="product_recall_detail"),
    url(r'products/$', RecallListView.as_view(model=ProductRecall), name="product_recall_list"),
    url(r'cars/$', RecallListView.as_view(model=CarRecall), name="car_recall_list"),
    url(r'food/$', RecallListView.as_view(model=FoodRecall), name="food_recall_list"),
    url(r'all/$', RecallListView.as_view(), name="recalls_list"),
    url(r'search/$', RecallSearchView.as_view(), name="recalls_search"),
    url(r'^', RecallHomePageView.as_view(), name="recalls_home"),
)
