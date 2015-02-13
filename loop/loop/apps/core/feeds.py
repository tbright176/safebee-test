from xml.sax.saxutils import quoteattr

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.encoding import iri_to_uri
from django.utils.html import escape
from django.utils.text import slugify
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.decorators.cache import cache_page, cache_control

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from social.models import (MostPopularItem, MostPopularRecall,
                           PopularLast7DaysItem)
from .models import Article, Slideshow, StreamItem, Category, Tag, LoopUser


class ShortTagEnabledXMLGenerator(SimplerXMLGenerator):
    def startElement(self, name, attrs, short_tag=False):
        self._write(u'<' + name)
        for (name, value) in attrs.items():
            self._write(u' %s=%s' % (name, quoteattr(value)))
        if not short_tag:
            self._write(u'>')
        else:
            self._write(u'/>')

    def addQuickElement(self, name, contents=None, attrs=None,
                        short_tag=False):
        "Convenience method for adding an element with no children"
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs, short_tag=short_tag)
        if contents is not None:
            self.characters(contents)
        if not short_tag:
            self.endElement(name)


class ExtendedRSSFeed(Rss201rev2Feed):
    """
    Extends RSS feed to add media:content element.
    """
    def write(self, outfile, encoding):
        handler = ShortTagEnabledXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")

    def rss_attributes(self):
        attrs = super(ExtendedRSSFeed, self).rss_attributes()
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        if 'media_content' in item:
            handler.addQuickElement(u'media:content',
                                    attrs=item['media_content'],
                                    short_tag=True)


class CacheControlledFeed(Feed):

    @method_decorator(cache_control(max_age=settings.CACHE_CONTROL_MAX_AGE))
    @method_decorator(cache_page(settings.CACHE_CONTROL_MAX_AGE))
    def __call__(self, request, *args, **kwargs):
        return super(CacheControlledFeed, self)\
            .__call__(request, *args, **kwargs)


class LoopContentFeed(CacheControlledFeed):
    feed_type = ExtendedRSSFeed

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_categories(self, item):
        return (item.category,)

    def item_description(self, item):
        return escape(item.content_object.description)

    def item_pubdate(self, item):
        return item.publication_date

    def item_extra_kwargs(self, item):
        extra = {}
        try:
            image = item.promo_image.asset
            image = get_thumbnailer(image)\
                .get_thumbnail({'size': (600, 400),
                                'crop': 'smart',
                                'quality': 65})
            extra = {'media_content':\
                     {'url': iri_to_uri(image.url.replace(' ', '%20')),
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


class MostPopularFeed(CacheControlledFeed):
    link = "/feeds/most-popular/"
    title = "The most popular posts on SafeBee at this moment."

    def items(self):
        return MostPopularItem.notrecalls.all()[:10]

    def item_link(self, item):
        return item.link


class MostPopularRecallsFeed(CacheControlledFeed):
    link = "/feeds/most-popular-recalls/"
    title = "The most popular recalls on SafeBee at this moment."

    def items(self):
        return MostPopularRecall.objects.all()[:10]

    def item_link(self, item):
        return item.link


class PopularLast7DaysFeed(LoopContentFeed):
    link = "/feeds/popular-last-7-days/"
    title = "The most popular content from across all SafeBee categories over the last 7 days"

    def items(self):
        return PopularLast7DaysItem.objects.all()

    def item_author_name(self, item):
        return item.content_object.author.get_full_name()

    def item_categories(self, item):
        return (item.content_object.category,)

    def item_description(self, item):
        return escape(item.content_object.description)

    def item_pubdate(self, item):
        return item.content_object.publication_date

    def item_extra_kwargs(self, item):
        extra = {}
        try:
            image = item.content_object.promo_image.asset
            image = get_thumbnailer(image)\
                .get_thumbnail({'size': (600, 400),
                                'crop': 'smart',
                                'quality': 65})
            extra = {'media_content':\
                     {'url': iri_to_uri(image.url.replace(' ', '%20')),
                      'height': '%s' % image.height,
                      'width': '%s' % image.width,
                      'fileSize': '%s' % image.size,
                      'type': 'image/jpeg'}}
        except InvalidImageFormatError:
            pass
        return extra
