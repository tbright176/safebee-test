import json

from collections import OrderedDict

from django import template
from django.conf import settings
from django.contrib.sites.models import Site

from ..db_settings import GoogleGraphCorporate, GoogleGraphSocial

register = template.Library()


SCHEMA_TYPES = {
    'Article': 'Article',
    'Blog': 'Blog',
    'PhotoOfTheDay': 'Photograph',
    'Recipe': 'Recipe',
    'Slideshow': 'ImageGallery',
}


@register.inclusion_tag('includes/seo/schema_markup_json_ld.html')
def schema_markup_for_flatpage(flatpage, schema_type):
    current_site = Site.objects.get_current()
    info = OrderedDict()
    info["@context"] = "http://schema.org"
    info["@type"] = schema_type
    info["name"] = flatpage.title
    info["url"] = "http://%s%s" % (current_site.domain, flatpage.url)
    if flatpage.description:
        info["about"] = flatpage.description
    info["lastReviewed"] = flatpage.modification_date.isoformat()
    info["dateModified"] = flatpage.modification_date.isoformat()

    return {'schema_json': json.dumps(info, indent=4),
            'should_render': True}


@register.inclusion_tag('includes/seo/schema_markup_json_ld.html')
def schema_markup_for_author(author):
    current_site = Site.objects.get_current()
    info = OrderedDict()
    info["@context"] = "http://schema.org"
    info["@type"] = "Person"
    info["name"] = author.get_full_name()
    info["url"] = "http://%s%s" % (current_site.domain, author.get_absolute_url())
    # if author.profile_image or author.team_image or author.blogger_caricature:
    #     image_attributes = [author.profile_image, author.team_image, author.blogger_caricature]
    #     image_asset = next(attrib for attrib in image_attributes if attrib is not None)
    #     if image_asset:
    #         info["image"] = image_asset.asset.url
    return {'schema_json': json.dumps(info, indent=4),
            'should_render': True}


@register.inclusion_tag('includes/seo/schema_markup_json_ld.html', takes_context=True)
def schema_markup(context):
    content_item = context.get('content_item')
    if not content_item:
        return {'should_render': False}

    class_name = content_item.__class__.__name__
    if content_item.category and content_item.category.name == 'Recipes':
        class_name = 'Recipe'
    info = OrderedDict()
    info["@context"] = "http://schema.org"
    info["@type"] = SCHEMA_TYPES.get(class_name, "Article")
    info["name"] = content_item.get_title()
    info["headline"] = content_item.get_title()
    info["url"] = content_item.get_fully_qualified_url()
    if info["@type"] == 'Article':
        info["articleSection"] = content_item.category.name
    info["about"] = u"%s" % content_item.description
    info["author"] = content_item.author.get_full_name()
    info["datePublished"] = content_item.publication_date.isoformat()

    if content_item.primary_image or content_item.promo_image:
        if content_item.primary_image:
            info["image"] = content_item.primary_image.asset.url
        elif content_item.promo_image:
            info["image"] = content_item.promo_image.asset.url

    addl_item = context.get('current_slide')
    if addl_item:
        if hasattr(addl_item, "image"):
            info["primaryImageOfPage"] = addl_item.image.asset.url

    if content_item.subhead:
        info['alternativeHeadline'] = content_item.subhead

    return {'schema_json': json.dumps(info, indent=4),
            'should_render': not info["@type"] == 'Recipe'}


@register.inclusion_tag('includes/seo/breadcrumb_markup.html', takes_context=True)
def schema_breadcrumb(context):

    current_site = Site.objects.get_current()
    content_item = context.get('content_item')

    hierarchy = [
        {
            'url': '{}'.format(current_site.domain),
            'title': current_site.name,
        },
     ]

    if content_item:
        for obj in [content_item.category.parent, content_item.category]:
            if obj:
                hierarchy.append({
                    'url': '{}{}'.format(
                        current_site.domain,
                        obj.get_absolute_url()
                    ),
                    'title': obj.name
                })

    return { 'hierarchy': hierarchy }

@register.inclusion_tag('includes/seo/google_knowledge_graph.html')
def google_knowledge_graph():
    site = Site.objects.first()
    corp_graph = GoogleGraphCorporate()

    schema = {
        '@context': 'http://schema.org',
        '@type': 'Organization',
        'url': 'http://{}'.format(site.domain),
        'name': corp_graph.organization_name,
        'logo': '{}{}'.format(settings.STATIC_URL, corp_graph.logo),
        'sameAs': [],
        'contactPoint': [],
    }

    if corp_graph.sales_phone_number:
        contact = {
            '@type': 'ContactPoint',
            'telephone': corp_graph.sales_phone_number,
            'contactType': 'sales',
        }
        schema['contactPoint'].append(contact)

    social_graph = GoogleGraphSocial()

    for social_url in social_graph.values():
        if social_url:
            schema['sameAs'].append(social_url)

    return {'google_knowledge_graph': json.dumps(schema, indent=4)}
