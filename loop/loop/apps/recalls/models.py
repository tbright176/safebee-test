import datetime
import logging
import requests

from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse as date_parse
from easy_thumbnails.fields import ThumbnailerImageField
from itertools import ifilter

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, post_delete
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

    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    updated = models.DateTimeField(auto_now=True,
                                   db_index=True)

    class Meta:
        abstract = True

    def title(self):
        if self.recall_subject:
            return self.recall_subject
        return self.name

    def post_parse(self, result_json):
        try:
            self.image.file
        except ValueError:
            self.retrieve_image('http://placehold.it/500x500')

        self.save()

    def retrieve_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            self.image.save(response.request.url.split('/')[-1],
                            File(img_temp), save=True)
        else:
            logger.error('Non 200 while trying to retrieve: {}'.format(image_url))


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
        super(FoodRecall, self).post_parse(result_json)


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

    def scrape_old_template(self, soup_obj):
        pot_subject = soup_obj.find('h2')
        if pot_subject:
            self.recall_subject = pot_subject.text

        # Extract contact summary
        strong_fields = soup_obj.findAll('strong')

        for strong_tag in strong_fields:
            if strong_tag.text.startswith('Contact:'):
                self.contact_summary = strong_tag.nextSibling

            if strong_tag.text.startswith('Remedy:'):
                self.corrective_summary = strong_tag.nextSibling


    def scrape_new_template(self, soup_obj):
        """
        Parse the new (and hopefully current) version of the CPSC product detail
        page.
        """

        title_tag = soup_obj.find('meta', {'property': 'og:title'})
        if title_tag:
            self.recall_subject = title_tag.get('content')

        # Extract contact summary from details section
        labels = soup_obj.findAll('span', {'class': 'lbl'})
        for label in labels:
            if 'Consumer Contact:' in label.text:
                pot_children = ifilter(lambda x: hasattr(x, 'text'),
                                       [tag for tag in label.nextSiblingGenerator()])
                self.contact_summary = ' '.join([tag.text for tag in pot_children])
                break

    def post_parse(self, result_json):
        """
        Post parsing activities. Retrive extra info from recall_url.

        Sadly, the product API returns are inadequate. Extra calls to scrape the
        CPSC site for needed information are performed here. The extra bits of
        information that we need are:
         - product images
         - recall subject
         - contact summary

        """

        if not self.name:
            self.name = self.descriptions

        # determine the product recall template version via date
        # Before 10-1-2012 -> version 1
        # After 10-1-2012 -> version 2
        # ConceptDemo -> We ain't interested in no concept demos
        # ^^ is actually a search result link that we can't handle.
        # maybe we should email an admin or stick in a queue to get
        # manually updated.
        if self.recall_url and 'ConceptDemo' not in self.recall_url:
            product_html = requests.get(self.recall_url).content
            soup = BeautifulSoup(product_html)
            page_images = soup.findAll('img')

            # the first and last images are header/footer images
            # everything else inbetween are product images
            if len(page_images) > 2: # header+footer images
                image_url = 'http://cpsc.gov{}'.format(page_images[1].get('src'))
                self.retrieve_image(image_url)

            if date_parse(str(self.recall_date)).date() < datetime.date(2014, 10, 1):
                self.scrape_old_template(soup)
            else:
                self.scrape_new_template(soup)

        if result_json['upcs']:
            for upc in result_json['upcs']:
                upc_record, _ = ProductUPC.objects.get_or_create(recall=self, upc=upc)

        super(ProductRecall, self).post_parse(result_json)


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

        super(CarRecall, self).post_parse(result_json)


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


class RecallStreamItem(models.Model):

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    organization = models.PositiveSmallIntegerField(choices=Recall.ORG_CHOICES, blank=True, null=True)
    recall_subject = models.TextField(blank=True)
    recall_number = models.CharField(db_index=True, max_length=50, blank=True)
    recall_url = models.URLField(blank=True)
    recall_date = models.DateField(blank=True, null=True)

    name = models.TextField(blank=True)
    initiator = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    corrective_summary = models.TextField(blank=True)
    consequence_summary = models.TextField(blank=True)
    defect_summary = models.TextField(blank=True)
    contact_summary = models.TextField(blank=True)

    image = ThumbnailerImageField(upload_to='assets/recalls/images',
                                  max_length=255, null=True, blank=True)

    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)


    def get_absolute_url(self):
        return reverse('recalls_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created']


from recalls.signals import create_stream_item, delete_stream_item

for cls in [ProductRecall, FoodRecall, CarRecall]:
    post_save.connect(create_stream_item, sender=cls)
    post_delete.connect(delete_stream_item, sender=cls)
