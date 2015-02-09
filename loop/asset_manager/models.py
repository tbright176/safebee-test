import datetime
import os

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from easy_thumbnails.fields import ThumbnailerImageField


class License(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name',]

    def __unicode__(self):
        return u"%s" % self.name


class Asset(models.Model):
    caption = models.TextField()
    display_caption = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True)
    notes = models.TextField(help_text="Optional. For internal use only.",
                             null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True,
                                             auto_now_add=True,
                                             verbose_name="last modified")

    # Attribution fields
    asset_author = models.CharField(max_length=255, null=True, blank=True)
    asset_source = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Author URL')
    asset_organization = models.CharField(max_length=255,
                                          null=True, blank=True)
    asset_organization_source = models.CharField(max_length=255,
                                                 null=True, blank=True,
                                                 verbose_name='Organization URL')
    asset_license = models.ForeignKey('License', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-creation_date']

    def __unicode__(self):
        return u"%s" % self.caption

    def asset_credit_string(self):
        output = render_to_string('image_credit.html', {'asset': self}).strip()
        return mark_safe(output)

    @property
    def asset(self):
        raise NotImplementedError(("Subclasses should implement this field to "
                                   "customize based on the type of asset."))

    def get_absolute_url(self):
        raise NotImplementedError(("Subclasses should implement this method to"
                                   " provide the absolute URL for the asset."))


def image_asset_storage_path(instance, filename, sub_path=False):
    """
    If sub_path is true, return a path that places the filename within a
    directory named after the instance.asset name.
    """
    today = datetime.datetime.today()
    initial_path = "assets/images/%d/%d" % (today.year, today.month)
    if instance.asset and sub_path:
        asset_basename = os.path.basename(instance.asset.name)
        basename = os.path.splitext(asset_basename)[0]
        return u'%s/%s/%s' % (initial_path, basename, filename)
    return u'%s/%s' % (initial_path, filename)


def image_asset_storage_subpath(instance, filename):
    return image_asset_storage_path(instance, filename, sub_path=True)


class Image(Asset):
    alt_text = models.CharField(max_length=255)
    asset = ThumbnailerImageField(upload_to=image_asset_storage_path,
                                  max_length=255,
                                  help_text=("Required. Upload a larger "
                                             "version of the asset than is "
                                             "needed, as it will be scaled "
                                             "and cropped automatically to "
                                             "fit the template as required."))
    social_asset = ThumbnailerImageField(upload_to=image_asset_storage_subpath,
                                         max_length=255, null=True, blank=True,
                                         help_text=("Optional. If defined, "
                                                    "this will be used as the "
                                                    "representation of the "
                                                    "image on social media."))
    promo_asset = ThumbnailerImageField(upload_to=image_asset_storage_subpath,
                                        max_length=255, null=True, blank=True,
                                         help_text=("Optional. If defined, "
                                                    "this will be used as the "
                                                    "representation of the "
                                                    "image in promo spots "
                                                    "across the site."))
    def get_absolute_url(self):
        return self.asset.url
