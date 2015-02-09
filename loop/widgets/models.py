from django.db import models

from loop.asset_manager.models import Image
from loop.core.models import StreamItem


class Widget(models.Model):
    label = models.CharField(max_length=100, unique=True)
    show_header = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.label


class PromoWidget(Widget):
    header_image = models.ForeignKey(Image, blank=True, null=True)


class PromoWidgetItem(models.Model):
    widget = models.ForeignKey(PromoWidget)
    content_item = models.ForeignKey(StreamItem)
    title = models.CharField(max_length=40, null=True, blank=True,
                             help_text=("Optional. Use to override the "
                                        "content_object's title."))
    link = models.URLField(null=True, blank=True,
                           help_text=("Optional. Use to override the "
                                      "content_object's URL. You may link to "
                                      "arbitrary URL in this field."))
    description = models.CharField(max_length=75, null=True, blank=True,
                                   help_text=("Optional. Use to override the "
                                              "content_object's description."))
    image = models.ForeignKey(Image, blank=True, null=True,
                              help_text=("Optional. Use to override the "
                                         "content_object's image."))
    order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def promo_title(self):
        if self.title:
            return u"%s" % self.title
        return u"%s" % self.content_item

    def promo_description(self):
        if self.description:
            return u"%s" % self.description
        return u"%s" % self.content_item.content_object.description

    def promo_url(self):
        if self.link:
            return u"%s" % self.link
        return u"%s" % self.content_item.get_absolute_url()

    def promo_image(self):
        if self.image:
            return self.image
        return self.content_item.promo_image

    def __unicode__(self):
        return self.promo_title()
