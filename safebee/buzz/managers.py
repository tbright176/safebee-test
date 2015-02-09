from django.db import models


class ActiveBuzzStoryManager(models.Manager):

    def get_queryset(self):
        return super(ActiveBuzzStoryManager, self)\
            .get_queryset().select_related('stream_item').filter(active=True)
