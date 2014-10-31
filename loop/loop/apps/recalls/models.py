import datetime
import logging
import requests

from BeautifulSoup import BeautifulSoup
from easy_thumbnails.fields import ThumbnailerImageField

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


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

    name = models.TextField(blank=True)
    initiator = models.TextField()
    notes = models.TextField()
    corrective_summary = models.TextField()
    consequence_summary = models.TextField()
    defect_summary = models.TextField()
    contact_summary = models.TextField(blank=True)

    image = ThumbnailerImageField(upload_to='assets/recalls/images',
                                  max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def post_parse(self, result_json):
        raise NotImplemented


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

    def post_parse(self, result_json):
        pass


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

    def post_parse(self, result_json):
        if self.recall_url:
            product_html = requests.get(self.recall_url).content
            soup = BeautifulSoup(product_html)

            # Extract subject from H2
            pot_subject = soup.find('h2')
            if pot_subject:
                self.recall_subject = pot_subject.text

            # Extract contact summary
            strong_fields = soup.findAll('strong')

            for strong_tag in strong_fields:
                if strong_tag.text.startswith('Contact:'):
                    self.contact_summary = strong_tag.nextSibling

                if strong_tag.text.startswith('Remedy:'):
                    self.corrective_summary = strong_tag.nextSibling

            page_images = soup.findAll('img')

            # the first and last images are header/footer images
            # everything else inbetween are product images
            if len(page_images) > 2: # header+footer images
                image_url = page_images[1].get('src')
                response = requests.get('http://cpsc.gov{}'.format(image_url))
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()
                    self.image.save(response.request.url.split('/')[-1],
                                    File(img_temp), save=True)
                else:
                    logger.error('Non 200 while trying to retrieve: {}'.format(image_url))

        if result_json['upcs']:
            for upc in result_json['upcs']:
                upc_record, _ = ProductUPC.objects.get_or_create(recall=self, upc=upc)


class ProductUPC(models.Model):
    recall = models.ForeignKey('ProductRecall')
    upc = models.CharField(_('UPC'), max_length=64, blank=True)


class CarRecall(Recall):
    code = models.CharField(_('code'), max_length=1)

    def __unicode__(self):
        return u'Car Recall <{}>'.format(self.recall_subject)

    def post_parse(self, result_json):
        for record_json in result_json['records']:
            record_json.update(recall=self)
            car_record, _ = CarRecallRecord.objects.get_or_create(
                recalled_component_id=record_json['recalled_component_id'],
                defaults=record_json
            )


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
