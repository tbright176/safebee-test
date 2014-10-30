import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField


class Recall(models.Model):

    CPSC = 0
    FDA = 1
    NHTSA = 2
    USDA = 3

    ORG_CHOICES = (
        (CPSC, 'CPSC'),
        (FDA, 'FDA'),
        (NHTSA, 'NHTSA'),
        (USDA, 'USDA')
    )

    organization = models.PositiveSmallIntegerField(choices=ORG_CHOICES)

    recall_subject = models.TextField()
    recall_number = models.CharField(db_index=True, max_length=50)
    recall_url = models.URLField()
    recall_date = models.DateField()

    initiator = models.TextField()
    notes = models.TextField()
    corrective_summary = models.TextField()
    consequence_summary = models.TextField()
    defect_summary = models.TextField()

    image = ThumbnailerImageField(upload_to='assets/recalls/images',
                                  max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class FoodRecall(Recall):
    FOOD = 'F'
    DRUG = 'D'

    FOOD_TYPES = (
        (FOOD, 'Food'),
        (DRUG, 'Drug'),
    )
    food_type = models.CharField(_('Food Recall Type'),
                                 max_length=1, blank=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    def __unicode__(self):
        return u'Food Recall <{}>'.format(self.summary)


class ProductRecall(Recall):

    manufacturers = models.TextField(blank=True)
    product_types = models.TextField(blank=True)
    descriptions = models.TextField(blank=True)
    hazards = models.TextField(blank=True)
    countries = models.TextField(blank=True)

    def __unicode__(self):
        return u'Product Recall <{}:{}>'.format(
            self.manufacturers,
            self.descriptions
        )

    def get_absolute_url(self):
        return reverse('recalls_detail', kwargs={'pk': self.pk})


class ProductUPC(models.Model):
    recall = models.ForeignKey('ProductRecall')
    upc = models.CharField(_('UPC'), max_length=64, blank=True)


class CarRecall(Recall):
    code = models.CharField(_('code'), max_length=1)

    def __unicode__(self):
        return u'Car Recall <{}>'.format(self.recall_subject)


class CarRecallRecord(models.Model):
    recalled_component_id = models.CharField(_('recall component identifier'),
                                             max_length=50)
    recall = models.ForeignKey('CarRecall')

    component_description = models.TextField(_('component description'))
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    manufacturing_begin_date = models.DateField(_('manufacturing begin date'),
                                                blank=True, null=True)
    manufacturing_end_date = models.DateField(_('manufacturing end date'),
                                              blank=True, null=True)
    make = models.CharField(_('make'), max_length=50, blank=True)
    model = models.CharField(_('model'), max_length=50, blank=True)

    year = models.PositiveSmallIntegerField(_('year'), max_length=4,
                                            blank=True, null=True)
