import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    recall_subject = models.CharField(max_length=50)
    recall_number = models.CharField(db_index=True, max_length=50)
    recall_url = models.URLField()
    recall_date = models.DateField() # format 2014-10-01

    initiator = models.CharField(max_length=50)
    notes = models.TextField()
    corrective_summary = models.TextField()
    consequence_summary = models.TextField()
    defect_summary = models.TextField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"<{0}> - {1}".format(
            self.recall_number,
            self.recall_subject
        )


class FoodRecall(Recall):
    FOOD = 'F'
    DRUG = 'D'

    FOOD_TYPES = (
        (FOOD, 'Food'),
        (DRUG, 'Drug'),
    )
    food_type = models.CharField(_('Food Recall Type'), max_length=1, blank=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)


class ProductRecall(Recall):
    pass


class ProductUPC(models.Model):
    recall = models.ForeignKey('ProductRecall')
    upc = models.CharField(_('UPC'), max_length=64, blank=True)


class CarRecall(Recall):
    code = models.CharField(_('code'), max_length=1)


class CarRecallRecord(models.Model):
    recalled_component_id = models.CharField(_('recall component identifier'), max_length=50)
    recall = models.ForeignKey('CarRecall')

    component_description = models.CharField(_('component description'), max_length=50)
    manufacturer = models.CharField(_('manufacturer'), max_length=100)
    manufacturing_begin_date = models.DateField(_('manufacturing begin date'), blank=True)
    manufacturing_end_date = models.DateField(_('manufacturing end date'), blank=True)
    make = models.CharField(_('make'), max_length=50, blank=True)
    model = models.CharField(_('model'), max_length=50, blank=True)
    year = models.PositiveSmallIntegerField(_('year'), max_length=4, blank=True)
