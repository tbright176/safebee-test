from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save

from loop.asset_manager.models import Image
from loop.core.models import Content, StreamItem


class Feature(Content):

    def get_absolute_url(self):
        class_name = self.__class__.__name__.lower()
        kwargs = self.build_default_url_kwargs()
        return reverse_lazy('features_%s' % class_name, kwargs=kwargs)

    def get_primary_featured_item(self):
        """
        If an item is not set as the primary feature, return the first
        item amongst the featured items.
        """
        primary_feature = self.featureditem_set.filter(primary_feature=True)
        if primary_feature:
            return primary_feature[0]
        else:
            return self.featureditem_set.first()

    def get_featured_items(self):
        """
        Excludes primary featured item if exists, otherwise returns all but
        the first item (first item defaults to primary featured if none was
        explicitly set.
        """
        primary_feature = self.featureditem_set.filter(primary_feature=True)
        if primary_feature:
            primary_id = primary_feature[0]
            return self.featureditem_set.exclude(pk=primary_id.id)
        else:
            return self.featureditem_set.all()[1:]


class FeaturedItem(models.Model):
    feature = models.ForeignKey(Feature)
    content_item = models.ForeignKey(StreamItem)
    order = models.PositiveIntegerField()
    primary_feature = models.BooleanField(default=False)

    # overrides
    image = models.ForeignKey(Image, null=True, blank=True,
                              related_name=("%(app_label)s_%(class)s_image"),
                              on_delete=models.SET_NULL,
                              help_text=("Optional. Use to override the "
                                        "content item's image."))
    title = models.CharField(max_length=255, null=True, blank=True,
                             help_text=("Optional. Use to override the "
                                        "content item's title."))
    url = models.URLField(null=True, blank=True,
                          help_text=("Optional. Use to override the "
                                     "content item's URL. You may link to an "
                                     "arbitrary URL in this field."))

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        if self.title:
            return u"%s" % self.title
        else:
            return u"%s" % self.content_item

    def get_image(self):
        if self.image:
            return self.image
        else:
            return self.content_item.promo_image

    def get_absolute_url(self):
        if self.url:
            return self.url
        else:
            return self.content_item.get_absolute_url()


from loop.core.signals import (create_stream_item, delete_stream_item,
                               update_stream_item_m2m, tweet_content)

m2m_changed.connect(update_stream_item_m2m, sender=Feature.tags.through)
post_save.connect(create_stream_item, sender=Feature)
post_save.connect(tweet_content, sender=Feature)
post_delete.connect(delete_stream_item, sender=Feature)
