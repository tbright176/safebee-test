import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Recall(models.Model):

    CPSC = 1
    FDA = 2
    NHTSA = 3
    USDA = 4

    ORG_CHOICES = (
        (CPSC, 'CPSC'),
        (FDA, 'FDA'),
        (NHTSA, 'NHTSA'),
        (USDA, 'USDA')
    )

    organization = models.PositiveSmallIntegerField(choices=ORG_CHOICES)

    recall_subject = models.CharField(max_length=50)
    recall_number = models.CharField(max_length=50)
    recall_url = models.URLField()
    recall_date = models.DateField() # format 2014-10-01
    report_date = models.DateField() # format 20141001 :/
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
    food_type = models.PositiveSmallIntegerField(_('Food Recall Type'), choices=FOOD_TYPES)


class ProductRecall(Recall):
    upc = models.CharField(max_length=64, blank=True)


class CarRecall(Recall):

    YEAR_CHOICES = [r for r in range(1900, datetime.datetime.now().year+2)]

    make = models.CharField(_('make'), max_length=50, blank=True)
    model = models.CharField(_('model'), max_length=50, blank=True)
    #year = models.PositiveSmallIntegerField(_('year'), max_length=4, choices=YEAR_CHOICES)
    code = models.CharField(_('code'), max_length=1)
