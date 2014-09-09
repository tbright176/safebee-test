from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


SOCIAL_SERVICE_CHOICES = (
    ('T', 'Twitter'),
)


class SocialStatusRecord(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    social_service = models.CharField(max_length=2,
                                      choices=SOCIAL_SERVICE_CHOICES)
    action_completed = models.BooleanField(default=False)
