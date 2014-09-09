from django.db import models


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='P')


class DraftManager(models.Manager):

    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='D')


class ScheduledManager(models.Manager):

    def get_queryset(self):
        return super(ScheduledManager, self).get_queryset().filter(status='S')


class ModerationManager(models.Manager):

    def get_queryset(self):
        return super(ModerationManager, self)\
            .get_queryset().filter(status__in=['M', 'M1', 'M2', 'F', 'R'])


# Stream Customized Promotional Managers
class SitemapPublishedManager(PublishedManager):

    def get_queryset(self):
        return super(SitemapPublishedManager, self)\
            .get_queryset().filter(noindex=False, exclude_from_sitemap=False)


class RSSPublishedManager(PublishedManager):

    def get_queryset(self):
        return super(RSSPublishedManager, self)\
            .get_queryset().filter(exclude_from_rss=False)
