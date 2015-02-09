from urlparse import urlparse

from django import template
from django.template.loader import render_to_string

from loop.widgets.models import PromoWidgetItem


register = template.Library()


@register.simple_tag()
def promo_widget(promo_label, template_name='widgets/promo_widget.html'):
    promo = None
    promo_items = None
    promo_items = PromoWidgetItem.objects.filter(widget__label=promo_label)\
        .select_related('widget',
                        'content_item',
                        'content_item__content_object',
                        'content_item__content_object__category',
                        'content_item__content_object__author',
                        'content_item__content_object__promo_image',
                        'image').all()
    if promo_items:
        promo = promo_items[0].widget
        for item in promo_items:
            if item.link:
                hostname = urlparse(item.link).netloc.replace('www.', '')
                setattr(item, 'hostname', hostname)


    return render_to_string(template_name, {
        'promo': promo,
        'promo_items': promo_items,
    })
