from django.db import models

from core.models import StreamItem

from .managers import ActiveBuzzStoryManager


class BuzzStory(models.Model):
    stream_item = models.ForeignKey(StreamItem, unique=True)
    active = models.BooleanField(default=False)

    objects = models.Manager()
    activated = ActiveBuzzStoryManager()

    class Meta:
        ordering = ['-active', 'stream_item']
        verbose_name_plural = 'Buzz Stories'

    def __unicode__(self):
        return u"%s" % self.stream_item

    def category(self):
        return self.stream_item.category

    def image(self):
        return self.stream_item.promo_image

    def url(self):
        return self.stream_item.get_absolute_url()
