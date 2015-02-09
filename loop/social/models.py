from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .managers import MostPopularNotRecallsManager


SOCIAL_SERVICE_CHOICES = (
    ('D', 'Disqus'),
    ('T', 'Twitter'),
)

DISQUS_THREAD_TYPES = (
    ('H', 'Hot'),
    ('P', 'Popular'),
)


class SocialStatusRecord(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    social_service = models.CharField(max_length=2,
                                      choices=SOCIAL_SERVICE_CHOICES)
    action_completed = models.BooleanField(default=False)


class DisqusThread(models.Model):
    order = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField()
    thread_type = models.CharField(max_length=2, choices=DISQUS_THREAD_TYPES)
    thread_link = models.URLField()
    thread_posts = models.PositiveIntegerField(default=0)
    thread_likes = models.PositiveIntegerField(default=0)
    thread_title = models.CharField(max_length=255)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u"%s" % self.thread_title


class MostPopularItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    link = models.URLField()

    objects = models.Manager()
    notrecalls = MostPopularNotRecallsManager()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u"%s" % self.title


class MostPopularRecall(MostPopularItem):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
