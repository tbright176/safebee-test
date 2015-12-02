from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.utils import timezone
from django.utils.text import slugify

from asset_manager.models import Image
from .managers import (DraftManager, ModerationManager,
                       PublishedManager, ScheduledManager,
                       RSSPublishedManager, SitemapPublishedManager)


class LoopUser(AbstractUser):
    title = models.CharField(max_length=40, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles", null=True, blank=True,
                                      help_text="Image should be large, preferably 640x640 or larger. Please ensure the photo will work well in a square aspect ratio.")
    bio = models.TextField(null=True, blank=True)
    include_on_about_page = models.BooleanField(default=False, help_text="Enable to include this user on the About Us page")
    inclusion_ordering = models.PositiveSmallIntegerField(default=0,
                                                          help_text="For users included on the about page, this field controls the ordering. If two or more users share the same order, then they will be sorted alphabetically.")
    google_plus_profile_url = models.URLField(null=True, blank=True,
                                              help_text="Google+ Profile URL")
    twitter = models.CharField(max_length=50, null=True, blank=True,
                               help_text="Twitter username")

    class Meta(AbstractUser.Meta):
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        if self.get_full_name():
            return u"%s" % self.get_full_name()
        else:
            return super(LoopUser, self).__unicode__()

    def get_absolute_url(self):
        name_slug = slugify(self.get_full_name())
        return reverse('core_author_index', kwargs={'author_slug': name_slug})

    def is_editor(self):
        if self.is_superuser:
            return True

        try:
            editor_group = self.groups.get(name='Editors')
        except Group.DoesNotExist:
            return False
        return True


class PublicationDateModel(models.Model):
    """
    Abstract model for use as mixin for models that need date tracking.
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(default=timezone.now,
                                            db_index=True)
    modification_date = models.DateTimeField(auto_now=True,
                                             auto_now_add=True,
                                             verbose_name="last modified")

    class Meta:
        abstract = True
        ordering = ['-publication_date']


PUBLISHING_CHOICES = (
    ('D', 'Draft'),
    ('M', 'Moderate'),
    ('P', 'Published'),
    ('S', 'Scheduled'),
)


class PublicationStatusModel(models.Model):
    """
    Abstract model for use as mixin for models that need a publication status.
    """
    status = models.CharField(max_length=2, choices=PUBLISHING_CHOICES,
                              default='D')

    class Meta:
        abstract = True


class Content(PublicationDateModel, PublicationStatusModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    secondary_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    basename = models.SlugField(max_length=255,
                                help_text=("By default, this field is auto-"
                                           "generated from the title."))
    category = models.ForeignKey('Category')
    subhead = models.CharField(max_length=255, null=True, blank=True)
    teaser = models.CharField(max_length=255, null=True, blank=True,
                              help_text=("Optional. If not set, the contents "
                                         "of the description field will be "
                                         "used."))
    tags = models.ManyToManyField("Tag", null=True, blank=True)
    notes = models.TextField(null=True, blank=True,
                             help_text=("For internal notes only."))

    # Image fields
    primary_image = models.ForeignKey(Image, null=True, blank=True,
                                      related_name=("%(app_label)s_%(class)s_primary_image"), on_delete=models.SET_NULL)
    promo_image = models.ForeignKey(Image, null=True, blank=True,
                                    related_name=("%(app_label)s_%(class)s_promo_image"),
                                    help_text=("Optional. If left blank, the "
                                               "promo image will be "
                                               "automatically created from "
                                               "the primary image."),
                                    on_delete=models.SET_NULL)
    social_image = models.ForeignKey(Image, null=True, blank=True,
                                     related_name=("%(app_label)s_%(class)s_social_image"),
                                     help_text=("Optional. If left blank, the "
                                                "social image will be "
                                                "automatically created from "
                                                "the primary image."),
                                     on_delete=models.SET_NULL)

    # SEO/meta fields
    canonical_url = models.URLField(verbose_name='Canonical URL',
                                    null=True, blank=True,
                                    help_text=("Optional. If left blank, the "
                                               "content's auto-generated URL "
                                               "will be used."))
    news_keywords = models.CharField(max_length=255, null=True, blank=True,
                                     help_text=("Enter a comma separated "
                                                "list of keywords (no more"
                                                " than 10) for this page."))
    description = models.CharField(max_length=160, unique=True,
                                   help_text=("This text will be used as the "
                                              "content's meta description for "
                                              "SEO purposes"))
    enable_standout_tag = models.BooleanField(default=False)
    noodp_noydir = models.BooleanField(default=True,
                                       verbose_name="NOODP/NOYDIR")
    nofollow = models.BooleanField(default=False)
    noindex = models.BooleanField(default=False)
    page_title = models.CharField(max_length=255, null=True, blank=True,
                                  help_text=("Optional. Use this to customize"
                                             " the title displayed in the"
                                             " page's &lt;title&gt; tag."))

    # Promotional Settings
    exclude_from_home_page = models.BooleanField(default=False)
    exclude_from_rss = models.BooleanField(default=False)
    exclude_from_newsletter_rss = models.BooleanField(default=False)
    exclude_from_twitter = models.BooleanField(default=False)
    exclude_from_sitemap = models.BooleanField(default=False)
    exclude_from_most_popular = models.BooleanField(default=False)

    # Page Settings
    disable_comments = models.BooleanField(default=False,
                                           help_text=(
                                               "Check to disable comments on "
                                               "this piece of content."))
    hide_right_rail = models.BooleanField(default=False,
                                          help_text=(
                                              "Check to hide the right rail "
                                              "on this page."))

    # Managers
    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()
    scheduled = ScheduledManager()
    needs_moderation = ModerationManager()
    sitemap = SitemapPublishedManager()
    rss = RSSPublishedManager()

    class Meta:
        abstract = True
        ordering = ['-publication_date']
        unique_together = (("category", "basename"),)

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        if self.pk is not None and self.status == 'P':
            try:
                old = self.__class__.objects.get(pk=self.id)
            except self.__class__.DoesNotExist:
                # this occurs when recovering deleted
                # content via django-reversion
                pass
            else:
                old_path = old.get_absolute_url()
                new_path = self.get_absolute_url()
                if not old_path == new_path:
                    site = Site.objects.get_current()
                    redirect, created = Redirect.objects.\
                                        get_or_create(site=site,
                                                      old_path=old_path)
                    redirect.new_path = new_path
                    redirect.save()
        super(Content, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.title

    def identifier(self):
        """
        Provides an identifier in the format of app_label::class::pk. This
        gives us a unique representation of an object uniquely regardless of
        basename or other changes to a content item.
        """
        debug = "DEBUG::" if settings.DEBUG else ""
        return "%s%s::%s::%s" % (debug, self._meta.app_label,
                                 self.__class__.__name__.lower(),
                                 self.id)

    def build_default_url_kwargs(self):
        kwargs = {'basename': self.basename}
        if self.category.parent:
            kwargs['category_slug'] = self.category.parent.slug
            kwargs['sub_category_slug'] = self.category.slug
        else:
            kwargs['category_slug'] = self.category.slug
        return kwargs

    def get_absolute_url(self):
        class_name = self.__class__.__name__.lower()
        kwargs = self.build_default_url_kwargs()
        return reverse('core_%s' % class_name, kwargs=kwargs)

    def get_fully_qualified_url(self):
        site = Site.objects.get_current()
        return "http://%s%s" % (site.domain, self.get_absolute_url())

    def get_canonical_url(self):
        if self.canonical_url:
            return self.canonical_url
        return self.get_fully_qualified_url()

    def get_title(self):
        if self.page_title:
            return self.page_title
        return self.title

    def get_related_content(self):
        return RelatedItem.objects.filter(object_id=self.id,
                                          content_type=ContentType.objects.get_for_model(self))


class Article(Content):
    body = models.TextField(null=True, blank=True)
    primary_image_caption_override =\
                                     models.TextField(max_length=255,
                                                      null=True, blank=True,
                                                      help_text="If set, this field will override the caption and credit provided by the primary image asset.")


class Blog(Content):
    body = models.TextField(null=True, blank=True)
    primary_image_caption_override =\
                                     models.TextField(max_length=255,
                                                      null=True, blank=True,
                                                      help_text="If set, this field will override the caption and credit provided by the primary image asset.")


class Infographic(Content):
    body = models.TextField(null=True, blank=True)


class PhotoOfTheDay(Content):
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)

    class Meta(Content.Meta):
        verbose_name = "Photo of the Day"
        verbose_name_plural = "Photos of the Day"


class PhotoBlog(Content):
    intro = models.TextField(blank=True)


class Photo(models.Model):
    photo_blog = models.ForeignKey('PhotoBlog')
    caption = models.TextField(null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True,
                              related_name=\
                              ("%(app_label)s_%(class)s_primary_image"),
                              on_delete=models.SET_NULL)
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['order',]
        unique_together = (('photo_blog', 'title'),)

    def __unicode__(self):
        return u"%s" % self.title


class TipsList(Content):
    pass


class TipsListItem(models.Model):
    tips_list = models.ForeignKey('TipsList')
    caption = models.TextField(null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True,
                              related_name=\
                              ("%(app_label)s_%(class)s_primary_image"),
                              on_delete=models.SET_NULL)
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['order',]
        unique_together = (('tips_list', 'title'),)

    def __unicode__(self):
        return u"%s" % self.title


class Slideshow(Content):
    pass


class Slide(models.Model):
    """
    Do we need meta/SEO stuff for these?
    """
    slideshow = models.ForeignKey('Slideshow')
    caption = models.TextField(null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True,
                              related_name=\
                              ("%(app_label)s_%(class)s_primary_image"),
                              on_delete=models.SET_NULL)
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['order',]
        unique_together = (('slideshow', 'title'),)

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        slideshow_kwargs = self.slideshow.build_default_url_kwargs()
        slideshow_kwargs['page_num'] = "%d" % (self.order + 1)
        return reverse('core_slideshow', kwargs=slideshow_kwargs)\
            .replace('page/1/', '')

    def get_fully_qualified_url(self):
        site = Site.objects.get_current()
        return "http://%s%s" % (site.domain, self.get_absolute_url())


class Taxonomy(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    meta_description = models.CharField(max_length=160,
                                        help_text="Max 160 characters.",
                                        null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.name

    def get_featured_content(self):
        return RelatedItem.objects.filter(object_id=self.id,
                                          content_type=ContentType.objects.get_for_model(self))


class Category(Taxonomy):

    class Meta:
        ordering = ['name',]
        verbose_name_plural = 'categories'

    def published_streamitem_set(self):
        return self.streamitem_set.filter(status="P")

    def get_absolute_url(self):
        kwargs = {}
        if self.parent:
            kwargs['category_slug'] = self.parent.slug
            kwargs['sub_category_slug'] = self.slug
        else:
            kwargs['category_slug'] = self.slug
        return reverse('core_category_index', kwargs=kwargs)


class Tag(Taxonomy):
    internal_use_only = models.BooleanField(default=False)

    class Meta:
        ordering = ['name',]

    def get_absolute_url(self):
        return reverse('core_tag_index', kwargs={'tag_slug': self.slug})


class StreamItem(models.Model):
    author = models.ForeignKey('LoopUser', null=True, blank=True,
                               related_name='author')
    secondary_author = models.ForeignKey('LoopUser', null=True, blank=True,
                                         related_name='secondary_author')
    category = models.ForeignKey('Category', null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    promo_image = models.ForeignKey(Image, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    publication_date = models.DateTimeField(default=timezone.now,
                                            db_index=True)
    status = models.CharField(max_length=2, choices=PUBLISHING_CHOICES,
                              default='D')
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", null=True, blank=True)

    noindex = models.BooleanField(default=False)

    # Promotional Settings
    exclude_from_home_page = models.BooleanField(default=False)
    exclude_from_rss = models.BooleanField(default=False)
    exclude_from_newsletter_rss = models.BooleanField(default=False)
    exclude_from_twitter = models.BooleanField(default=False)
    exclude_from_sitemap = models.BooleanField(default=False)
    exclude_from_most_popular = models.BooleanField(default=False)

    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()
    scheduled = ScheduledManager()
    needs_moderation = ModerationManager()
    sitemap = SitemapPublishedManager()
    rss = RSSPublishedManager()


    class Meta:
        ordering = ['-publication_date']

    def __unicode__(self):
        return u"%s" % self.title

    def content_type_identifier(self):
        return u"%s_%s" % (self.content_type.app_label,
                           self.content_type.model)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def should_display_byline(self):
        from features.models import Feature
        try:
            feature_ctype = ContentType.objects.get_for_model(Feature)
            if self.content_type == feature_ctype:
                return False
        except Exception, e:
            pass
        return True

class RelatedItem(models.Model):
    stream_item = models.ForeignKey('StreamItem', verbose_name="Content Item",
                                    null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')

    # override fields
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return u'%s' % self.get_title()

    def get_absolute_url(self):
        return self.stream_item.get_absolute_url()

    def get_title(self):
        title = self.stream_item.title
        if self.title:
            title = self.title
        return title

    def get_image(self):
        image = self.stream_item.promo_image
        if self.image:
            image = self.image
        return image


from .signals import (create_stream_item, delete_stream_item,
                      update_stream_item_m2m, tweet_content)

m2m_changed.connect(update_stream_item_m2m, sender=Article.tags.through)
post_save.connect(create_stream_item, sender=Article)
post_save.connect(tweet_content, sender=Article)
post_delete.connect(delete_stream_item, sender=Article)

m2m_changed.connect(update_stream_item_m2m, sender=PhotoOfTheDay.tags.through)
post_save.connect(create_stream_item, sender=PhotoOfTheDay)
post_save.connect(tweet_content, sender=PhotoOfTheDay)
post_delete.connect(delete_stream_item, sender=PhotoOfTheDay)

m2m_changed.connect(update_stream_item_m2m, sender=Slideshow.tags.through)
post_save.connect(create_stream_item, sender=Slideshow)
post_save.connect(tweet_content, sender=Slideshow)
post_delete.connect(delete_stream_item, sender=Slideshow)

m2m_changed.connect(update_stream_item_m2m, sender=Infographic.tags.through)
post_save.connect(create_stream_item, sender=Infographic)
post_save.connect(tweet_content, sender=Infographic)
post_delete.connect(delete_stream_item, sender=Infographic)

m2m_changed.connect(update_stream_item_m2m, sender=PhotoBlog.tags.through)
post_save.connect(create_stream_item, sender=PhotoBlog)
post_save.connect(tweet_content, sender=PhotoBlog)
post_delete.connect(delete_stream_item, sender=PhotoBlog)

m2m_changed.connect(update_stream_item_m2m, sender=TipsList.tags.through)
post_save.connect(create_stream_item, sender=TipsList)
post_save.connect(tweet_content, sender=TipsList)
post_delete.connect(delete_stream_item, sender=TipsList)

m2m_changed.connect(update_stream_item_m2m, sender=Blog.tags.through)
post_save.connect(create_stream_item, sender=Blog)
post_save.connect(tweet_content, sender=Blog)
post_delete.connect(delete_stream_item, sender=Blog)

from mastermind.models import Quiz
m2m_changed.connect(update_stream_item_m2m, sender=Quiz.tags.through)
post_save.connect(create_stream_item, sender=Quiz)
post_save.connect(tweet_content, sender=Quiz)
post_delete.connect(delete_stream_item, sender=Quiz)

from .db_settings import GoogleGraphCorporate, GoogleGraphSocial
GoogleGraphCorporate()
GoogleGraphSocial()
