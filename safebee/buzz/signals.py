from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BuzzStory
from loop.core.models import StreamItem


@receiver(post_save, sender=StreamItem, dispatch_uid='buzz_from_stream_item')
def create_buzz_story(sender, instance, signal, *args, **kwargs):
    if instance.status == 'P':
        bs, created = BuzzStory.objects.get_or_create(stream_item=instance)
    else:
        try:
            bs = BuzzStory.objects.get(stream_item=instance)
            bs.delete()
        except BuzzStory.DoesNotExist:
            pass
