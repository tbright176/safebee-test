from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.text import slugify

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from .models import Article, Slideshow, StreamItem, Category, Tag, LoopUser


class ExtendedRSSFeed(Rss201rev2Feed):
    """
    Extends RSS feed to add media:content element.
    """
    def rss_attributes(self):
        attrs = super(ExtendedRSSFeed, self).rss_attributes()
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        if 'media_content' in item:
            handler.addQuickElement(u'media:content', '',
                                    item['media_content'])


class LoopContentFeed(Feed):
    feed_type = ExtendedRSSFeed

    def item_extra_kwargs(self, item):
        extra = {}
        try:
            image = item.promo_image.asset
            image = get_thumbnailer(image)\
                .get_thumbnail({'size': (600, 400),
                                'crop': 'smart',
                                'quality': 65})
            extra = {'media_content':\
                     {'url': image.url,
                      'height': '%s' % image.height,
                      'width': '%s' % image.width,
                      'fileSize': '%s' % image.size,
                      'type': 'image/jpeg'}}
        except InvalidImageFormatError:
            pass
        return extra


class LatestContentFeed(LoopContentFeed):
    link = "/feeds/latest/"

    def title(self, obj):
        return "The Latest from %s" % Site.objects.get_current().name

    def items(self):
        return StreamItem.rss.all()[:settings.CORE_DEFAULT_FEED_LENGTH]


class CategoryFeed(LoopContentFeed):
    """
    A feed of all StreamItems belonging to the specified category.
    """
    def items(self, obj):
        stream_items = StreamItem.rss\
            .filter(Q(category=obj) | Q(category__parent=obj))[:settings.CORE_DEFAULT_FEED_LENGTH]
        return stream_items

    def link(self, obj):
        return reverse('core_category_feed', kwargs={'slug': obj.slug})

    def title(self, obj):
        return obj.name

    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)


class TagFeed(LoopContentFeed):
    """
    A feed of all StreamItems belonging to the specified tag.
    """
    def items(self, obj):
        stream_items = StreamItem.rss.filter(tags__in=[obj,])[:settings.CORE_DEFAULT_FEED_LENGTH]
        return stream_items

    def link(self, obj):
        return reverse('core_tag_feed', kwargs={'slug': obj.slug})

    def title(self, obj):
        return obj.name

    def get_object(self, request, slug):
        return get_object_or_404(Tag, slug=slug)


class AuthorFeed(LoopContentFeed):

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
        stream_items = StreamItem.rss.filter(author=obj)[:settings.CORE_DEFAULT_FEED_LENGTH]
        return stream_items

    def link(self, obj):
        return reverse('core_author_feed',
                       kwargs={'basename': slugify(obj.get_full_name())})

    def title(self, obj):
        return obj.get_full_name()
