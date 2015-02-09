from django.db import models

from loop.widgets.models import PromoWidget


class Module(models.Model):
    title = models.CharField(max_length=200)
    show_title = models.BooleanField(default=False,
                                     help_text="Show title bar above module")
    widget = models.ForeignKey(PromoWidget, null=True, blank=True)
    body = models.TextField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % self.title


class Rail(models.Model):
    # need to taxonomize?
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=255,
                           unique=True,
                           help_text="Use an absolute path without the domain name, e.g. /food-health/this-is-the-basename.html. If using a category path, like '/food-health/', be sure to include the trailing slash.")
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.title


class RailItem(models.Model):
    rail = models.ForeignKey('Rail', related_name='items')
    module = models.ForeignKey('Module')
    order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return u"%s" % self.module.title
