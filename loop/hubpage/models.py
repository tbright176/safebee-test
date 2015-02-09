from django.contrib.contenttypes.models import ContentType
from django.db import models

from asset_manager.models import Image
from core.models import Category, RelatedItem, StreamItem


class HubPage(models.Model):
    title = models.CharField(max_length=100)
    set_as_homepage = models.BooleanField(default=False)
    featured_content = models.ForeignKey(StreamItem, null=True, blank=True,
                                         help_text=("Optional. If you do not "
                                                    "select a featured story, "
                                                    "you must fill out all of "
                                                    "the fields below."))
    featured_content_title = models.CharField(max_length=255, null=True,
                                              blank=True,
                                              help_text=("Optional. Use to "
                                                         "override the featured "
                                                         "story's title."))
    featured_content_description =\
                                   models.CharField(max_length=255, null=True,
                                                    blank=True,
                                                    help_text=("Optional. Use "
                                                               "to override the "
                                                               "featured story's"
                                                               " description."))
    featured_content_image = models.ForeignKey(Image, null=True, blank=True,
                                               help_text=("Optional. Use to "
                                                          "override the featured"
                                                          " story's promo image."
                                                      )
    )
    featured_content_url = models.URLField(null=True, blank=True,
                                           help_text=("Optional. Use to override"
                                                      " the featured story's "
                                                      "URL."))
    hide_byline = models.BooleanField(default=False)

    def featured_title(self):
        if self.featured_content_title:
            return u"%s" % self.featured_content_title
        elif self.featured_content:
            return u"%s" % self.featured_content

    def featured_description(self):
        if self.featured_content_description:
            return u"%s" % self.featured_content_description
        elif self.featured_content:
            content_object = self.featured_content.content_object
            if content_object.teaser:
                return u"%s" % content_object.teaser
            else:
                return u"%s" % content_object.description

    def featured_image(self):
        if self.featured_content_image:
            return self.featured_content_image
        elif self.featured_content:
            return self.featured_content.promo_image

    def featured_url(self):
        if self.featured_content_url:
            return u"%s" % self.featured_content_url
        elif self.featured_content:
            return u"%s" % self.featured_content.get_absolute_url()

    def __unicode__(self):
        return u"%s" % self.title

    def get_featured_content(self):
        return RelatedItem.objects.filter(object_id=self.id,
                                          content_type=ContentType.objects.get_for_model(self))

class HubPageContentModule(models.Model):
    hubpage = models.ForeignKey('HubPage')
    module = models.ForeignKey('ContentModule')
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return u"%s" % self.module


class HubPageCategoryContentModule(models.Model):
    hubpage = models.ForeignKey('HubPage')
    module = models.ForeignKey('ContentModule')
    display_featured_story_only = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return u"%s" % self.module


class ContentModule(models.Model):
    hubpage = models.ForeignKey('HubPage', null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True,
                             help_text=("Optional. Leave blank to use the "
                                        "category title, or if no category is "
                                        "not set, display no title."))
    active = models.BooleanField(default=False, help_text=("Uncheck to remove "
                                                           "this module from "
                                                           "all pages it "
                                                           "displays on."))
    hide_featured_story_byline = models.BooleanField(default=False,
                                                     help_text=("Check to hide the featured story's byline on the category landing page."))

    def __unicode__(self):
        if self.title:
            return u"%s" % self.title
        elif self.category:
            return u"%s" % self.category.name
        else:
            return u""


class ContentModuleItem(models.Model):
    module = models.ForeignKey('ContentModule')
    featured = models.BooleanField(default=False)
    content_object = models.ForeignKey(StreamItem, null=True, blank=True,
                                       help_text=("Optional. If you do not "
                                                  "select a content object, "
                                                  "you must fill out all of the "
                                                  "fields below."))
    content_title = models.CharField(max_length=255, null=True,
                                     blank=True,
                                     help_text=("Optional. Use to override the "
                                                "content object's title."))
    content_description = models.CharField(max_length=255, null=True,
                                           blank=True,
                                           help_text=("Optional. Use to override"
                                                      " the content object's "
                                                      "description."))
    content_image = models.ForeignKey(Image, null=True, blank=True,
                                      help_text=("Optional. Use to override "
                                                 "the content object's promo "
                                                 "image."))
    content_url = models.URLField(null=True, blank=True,
                                  help_text=("Optional. Use to override the "
                                             "content object's URL."))
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def title(self):
        if self.content_title:
            return u"%s" % self.content_title
        elif self.content_object:
            return u"%s" % self.content_object.title

    def description(self):
        if self.content_description:
            return u"%s" % self.content_description
        elif self.content_object:
            content_object = self.content_object.content_object
            if content_object.teaser:
                return u"%s" % content_object.teaser
            else:
                return u"%s" % content_object.description

    def image(self):
        if self.content_image:
            return self.content_image
        elif self.content_object:
            return self.content_object.promo_image

    def url(self):
        if self.content_url:
            return self.content_url
        elif self.content_object:
            return self.content_object.get_absolute_url()

    def __unicode__(self):
        return self.title()
