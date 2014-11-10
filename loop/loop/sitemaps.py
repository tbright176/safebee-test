import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from core.models import Article, Category, LoopUser, Slideshow, StreamItem, Tag
from flatpages.models import FlatPage


class ArticleSitemap(Sitemap):
    limit = 2500
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.sitemap.all()

    def lastmod(self, obj):
        return obj.modification_date


class SlideshowSitemap(Sitemap):
    limit = 2500
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Slideshow.sitemap.all()

    def lastmod(self, obj):
        return obj.modification_date


class FlatPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return FlatPage.objects.filter(registration_required=False)

    def lastmod(self, obj):
        return obj.modification_date


class CategorySitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('core_category_index', args=[obj.slug])


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse('core_tag_index', args=[obj.slug])


class AuthorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        authors = StreamItem.sitemap.order_by('author__id')\
                  .values_list('author', flat=True).distinct()
        return LoopUser.objects.filter(pk__in=authors)
