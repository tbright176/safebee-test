from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from .models import Article, Slideshow, StreamItem, Category, Tag, LoopUser


class LatestContentFeed(Feed):
    link = "/feeds/latest/"

    def title(self, obj):
        return "The Latest from %s" % Site.objects.get_current().name

    def items(self):
        return StreamItem.rss.all()[:30]


class CategoryFeed(Feed):
    """
    A feed of all StreamItems belonging to the specified category.
    """
    def items(self, obj):
        stream_items = StreamItem.rss\
            .filter(Q(category=obj) | Q(category__parent=obj))[:30]
        return stream_items

    def link(self, obj):
        return reverse('core_category_feed', kwargs={'slug': obj.slug})

    def title(self, obj):
        return obj.name

    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)


class TagFeed(Feed):
    """
    A feed of all StreamItems belonging to the specified tag.
    """
    def items(self, obj):
        stream_items = StreamItem.rss.filter(tags__in=[obj,])[:30]
        return stream_items

    def link(self, obj):
        return reverse('core_tag_feed', kwargs={'slug': obj.slug})

    def title(self, obj):
        return obj.name

    def get_object(self, request, slug):
        return get_object_or_404(Tag, slug=slug)


class AuthorFeed(Feed):

    def get_object(self, request, basename):
        basename = slugify(basename)
        author = None
        users = LoopUser.objects.all()
        for user in users:
            if slugify(user.get_full_name()).find(basename) > -1:
                author = user
                break

        if not author:
            raise Http404

        return get_object_or_404(LoopUser, username=author.username)

    def items(self, obj):
        stream_items = StreamItem.rss.filter(author=obj)[:30]
        return stream_items

    def link(self, obj):
        return reverse('core_author_feed',
                       kwargs={'basename': slugify(obj.get_full_name())})

    def title(self, obj):
        return obj.get_full_name()
