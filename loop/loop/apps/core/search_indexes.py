import datetime

from django.conf import settings

from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import (Article, Blog, Infographic, PhotoOfTheDay,
                     PhotoBlog, Slideshow)


class SiteIndexMixin(object):
    site = indexes.CharField()

    def prepare_site(self, obj):
        return settings.HAYSTACK_APP_ID


class ContentIndex(CelerySearchIndex, SiteIndexMixin):
    """ Base Search Index class for all `Content` derived-models. """
    text = indexes.CharField(document=True, use_template=True)

    absolute_url = indexes.CharField(model_attr='get_fully_qualified_url')
    author = indexes.CharField(model_attr='author')
    category = indexes.CharField(model_attr='category__name')
    description = indexes.CharField(model_attr='description')
    modification_date = indexes.DateTimeField(model_attr='modification_date')
    primary_image = indexes.CharField(model_attr='primary_image', indexed=False, null=True)
    promo_image = indexes.CharField(indexed=False, null=True)
    publication_date = indexes.DateTimeField(model_attr='publication_date')

    teaser = indexes.CharField(model_attr='teaser')
    title = indexes.CharField(model_attr='get_title')

    def index_queryset(self, using=None):
        """ Only index published content. """
        return self.get_model().published.all()

    def get_updated_field(self):
        return 'modification_date'

    def prepare_promo_image(self, obj):
        if obj.promo_image:
            return obj.promo_image.get_absolute_url()


class BodyIndexMixin(object):
    """ Mixin for models with body fields. """
    body = indexes.CharField(model_attr='body')


class ArticleIndex(ContentIndex, BodyIndexMixin, indexes.Indexable):
    """ Search index for `Article` model. """

    def get_model(self):
        return Article


class BlogIndex(ContentIndex, BodyIndexMixin, indexes.Indexable):

    def get_model(self):
        return Blog


class InfographicIndex(ContentIndex, BodyIndexMixin, indexes.Indexable):

    def get_model(self):
        return Infographic


class PODIndex(ContentIndex, BodyIndexMixin, indexes.Indexable):

    subtitle = indexes.CharField(model_attr='subtitle', null=True)
    caption = indexes.CharField(model_attr='caption', null=True)

    def get_model(self):
        return PhotoOfTheDay


class PhotoBlogIndex(ContentIndex, indexes.Indexable):

    intro = indexes.CharField(model_attr='intro')
    body = indexes.CharField(model_attr='intro')

    def get_model(self):
        return PhotoBlog


class Slideshow(ContentIndex, indexes.Indexable):

    def get_model(self):
        return Slideshow
