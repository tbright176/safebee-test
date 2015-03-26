import math

from collections import OrderedDict

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.base import TextNode
from django.template.loader_tags import do_include

from hubpage.models import ContentModule
from ..models import Category, StreamItem

register = template.Library()


@register.simple_tag
def print_setting(name):
    return getattr(settings, name, "")


@register.tag('include_unless_debug')
def do_include_unless_debug(parser, token):
    if not settings.DEBUG:
        return do_include(parser, token)
    return TextNode('')


@register.simple_tag
def site_title_string():
    site = Site.objects.get_current()
    separator = settings.CORE_DEFAULT_SITE_TITLE_SEPARATOR
    return u"%s %s" % (separator, site.name)


@register.assignment_tag
def site_categories():
    categories = Category.objects.prefetch_related('streamitem_set').all()
    return categories


@register.assignment_tag
def get_next_content_item(current_content_object):
    next_item = None
    try:
        next_item = current_content_object\
            .get_next_by_publication_date(status='P')
    except current_content_object.__class__.DoesNotExist:
        pass
    return next_item


@register.assignment_tag
def get_previous_content_item(current_content_object):
    previous_item = None
    try:
        previous_item = current_content_object\
            .get_previous_by_publication_date(status='P')
    except current_content_object.__class__.DoesNotExist:
        pass
    return previous_item


@register.simple_tag
def nav_active(request, url):
    if request.path == '/' and url == '/':
        return 'active'
    elif not request.path == '/' and not url =='/' and request.path.find(url) >= 0:
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def previous_paginated_url(context, pagination_obj):
    site = Site.objects.get_current()
    if pagination_obj.has_previous:
        page_str = ''
        if pagination_obj.previous_page_number() == 1:
            page_str = ''
        else:
            page_str = "page/%s/" % pagination_obj.previous_page_number()
        return "http://%s%s%s" % (site.domain, context['request'].path.split('page/')[0], page_str)


@register.simple_tag(takes_context=True)
def next_paginated_url(context, pagination_obj):
    site = Site.objects.get_current()
    if pagination_obj.has_next:
        page_str = "page/%s/" % pagination_obj.next_page_number()
        return "http://%s%s%s" % (site.domain, context['request'].path.split('page/')[0], page_str)


@register.filter
def abbr_number(value):
    result = "%s" % value
    units = ["", "K", "M"]
    if value > 999:
        unit_index = math.floor(math.log(value, 1000))
        result = "%.1f%s" % ((value / math.pow(1000, unit_index)),
                             units[int(unit_index)])
        result = result.replace('.0', '')
        if result == "1000K":
            result = "1M"
    return result


@register.assignment_tag(takes_context=True)
def latest_stories(context, limit=4, exclude_content_item=None):
    items = StreamItem.published.select_related('author', 'category')
    if exclude_content_item:
        try:
            ct_type = ContentType.objects.get_for_model(exclude_content_item)
            items = items.exclude(object_id=exclude_content_item.id,
                                  content_type=ct_type)
        except:
            pass
    return items[:limit]


@register.assignment_tag(takes_context=True)
def latest_stories_for_category(context, limit=4, content_item=None):
    related_content = []
    if content_item:
        related_content = content_item.get_related_content()
        if related_content:
            related_content = [rc.stream_item for rc in related_content]
        else:
            related_content = []
    category = None
    if getattr(content_item, 'category', None):
        category = content_item.category
    items = StreamItem.published.select_related('author', 'category')
    if category:
        items = items.filter(category=category)
    if content_item:
        try:
            ct_type = ContentType.objects.get_for_model(content_item)
            items = items.exclude(object_id=content_item.id,
                                  content_type=ct_type)
        except:
            pass

    items = related_content + list(items[:limit])
    items = items[:limit]
    if len(items) < limit:
        latest_items = latest_stories(context, 40, content_item)
        if latest_items:
            latest_items = list(latest_items)
            items += latest_items
            items = list(OrderedDict.fromkeys(items))
    return items[:limit]


@register.assignment_tag
def featured_stories_for_category(category_name):
    category = Category.objects.get(name=category_name)
    module = ContentModule.objects.filter(category=category)
    if module:
        module = module[0]
        return module.contentmoduleitem_set.all()
