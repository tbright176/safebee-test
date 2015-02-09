from django.db import models


class MostPopularNotRecallsManager(models.Manager):

    def get_queryset(self):
        return super(MostPopularNotRecallsManager, self)\
            .get_queryset().exclude(link__startswith='/recall')
