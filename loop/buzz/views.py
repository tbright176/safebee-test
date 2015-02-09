from django.shortcuts import render
from django.views.generic.list import ListView

from core.views import CacheControlMixin
from .models import BuzzStory


class BuzzViewAll(ListView, CacheControlMixin):
    template_name = 'buzz.html'
    queryset = BuzzStory.activated.all()
