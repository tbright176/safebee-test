from django.contrib.contenttypes.models import ContentType

from loop.core.models import StreamItem
from loop.social.utils.tweet import tweet_obj, obj_was_tweeted


def tweet_content(sender, instance, signal, *args, **kwargs):
    if instance.status == 'P' and not instance.exclude_from_twitter:
        try:
            if not obj_was_tweeted(instance):
                tweet_obj(instance)
        except:
            pass


def create_stream_item(sender, instance, signal, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    stream_item, created = StreamItem.objects\
                                     .get_or_create(content_type=content_type,
                                                    object_id=instance.id)
    stream_item.author = instance.author
    stream_item.category = instance.category
    stream_item.publication_date = instance.publication_date
    stream_item.status = instance.status
    stream_item.title = instance.title
    stream_item.noindex = instance.noindex
    stream_item.exclude_from_home_page = instance.exclude_from_home_page
    stream_item.exclude_from_rss = instance.exclude_from_rss
    stream_item.exclude_from_newsletter_rss = instance.exclude_from_newsletter_rss
    stream_item.exclude_from_twitter = instance.exclude_from_twitter
    stream_item.exclude_from_sitemap = instance.exclude_from_sitemap
    stream_item.exclude_from_most_popular = instance.exclude_from_most_popular

    if instance.promo_image:
        stream_item.promo_image = instance.promo_image
    else:
        stream_item.promo_image = instance.primary_image

    stream_item.save()


def update_stream_item_m2m(sender, instance, action, reverse,
                           model, pk_set, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    stream_item, created = StreamItem.objects\
                                     .get_or_create(content_type=content_type,
                                                    object_id=instance.id)
    stream_item.tags = instance.tags.all()
    stream_item.save()


def delete_stream_item(sender, instance, signal, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    stream_item = StreamItem.objects.get(content_type=content_type,
                                         object_id=instance.id)
    stream_item.delete()
