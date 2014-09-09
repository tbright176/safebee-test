import urllib
from urlparse import urlparse

from django import template
from django.contrib.sites.shortcuts import get_current_site

from easy_thumbnails.files import get_thumbnailer

register = template.Library()


@register.simple_tag(takes_context=True)
def open_graph_type(context):
    pass


@register.simple_tag(takes_context=True)
def open_graph_image(context):
    """
    Return a fully-qualified image URL for use in the og:image meta
    tag. If content_item does not exist, a site-wide default will be
    returned instead.
    """
    # TODO: Do a default image URL here
    image_loc = ''

    if 'content_item' in context:
        content_item = context['content_item']
        if content_item.primary_image:
            image_asset = content_item.primary_image.asset

            if content_item.social_image:
                image_asset = content_item.social_image.asset
            elif content_item.primary_image.social_asset:
                image_asset = content_item.primary_image.social_asset

            thumbnail = get_thumbnailer(image_asset)['facebook_social_image']
            image_loc = u"%s" % thumbnail.url

    parsed = urlparse(image_loc)
    image_loc = image_loc.replace(parsed.path, urllib.quote(parsed.path))
    return image_loc
