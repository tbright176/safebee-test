import bitly_api

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from ..models import SocialStatusRecord


def fully_qualified_url_for_obj(obj):
    site = Site.objects.get_current()
    return "http://%s%s" % (site.domain, obj.get_absolute_url())


def action_completed_for_service(obj, service_identifier):
    was_completed = False
    ctype = ContentType.objects.get_for_model(obj)
    try:
        record = SocialStatusRecord.objects\
                                   .get(content_type=ctype,
                                        object_id=obj.id,
                                        social_service=service_identifier)
        was_completed = record.action_completed
    except SocialStatusRecord.DoesNotExist:
        pass

    return was_completed


def record_result(obj, service_identifier, result_boolean):
    ctype = ContentType.objects.get_for_model(obj)
    record, created = SocialStatusRecord.objects\
                                        .get_or_create(
                                            content_type=ctype,
                                            object_id=obj.id,
                                            defaults={'social_service': service_identifier})
    record.action_completed = result_boolean
    record.save()


def shorten_url(url):
    conn = bitly_api.Connection(settings.BITLY_API_USER,
                                settings.BITLY_API_KEY)
    try:
        resp = conn.shorten(url)
        if resp and 'url' in resp:
            return resp['url']
    except bitly_api.BitlyError:
        pass
