import datetime
import logging
import re
import requests

from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse as date_parse
from easy_thumbnails.files import get_thumbnailer
from itertools import ifilter

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.templatetags.static import static
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('loop.recalls')


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

    image = models.ImageField(upload_to='assets/recalls/images',
                              max_length=255, null=True, blank=True)

    slug = models.SlugField(max_length=255)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    updated = models.DateTimeField(auto_now=True,
                                   db_index=True)

    api_json = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-recall_date',]

    def title(self):
        if self.recall_subject:
            return self.recall_subject
        return self.name

    def post_parse(self, result_json):
        raise NotImplementedError

    def get_image(self, size=400):
        if self.image:

            thumbnailer = get_thumbnailer(self.image)
            opts = {
                'crop': 'smart',
                'size': (size, size),
            }
            thumbnail = thumbnailer.get_thumbnail(opts)
            return thumbnail.url

        return self.get_default_image(size=size)

    def get_image_95(self):
        return self.get_image(size=95)

    def get_image_90(self):
        return self.get_image(size=90)

    def get_image_55(self):
        return self.get_image(size=55)

    def get_image_60(self):
        return self.get_image(size=60)

    def get_image_65(self):
        return self.get_image(size=65)

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

    def get_default_image(self, size=400):
        return static(self.default_image_fmt.format(size))

    def get_default_image_55(self):
        return self.get_default_image(size=55)

    def get_default_image_65(self):
        return self.get_default_image(size=65)

    def get_default_image_90(self):
        return self.get_default_image(size=90)

    def get_default_image_95(self):
        return self.get_default_image(size=95)

    def should_create_stream_item(self):
        return True

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title()))
        super(Recall, self).save(*args, **kwargs)

    def get_fully_qualified_url(self):
        site = Site.objects.get_current()
        return "http://%s%s" % (site.domain, self.get_absolute_url())

    def get_canonical_url(self):
        return self.get_fully_qualified_url()


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
        return u"%s" % self.summary

    def get_absolute_url(self):
        return reverse('food_recall_detail',
                       kwargs={'slug': self.slug,
                               'recall_number': self.recall_number})

    def title(self):
        return self.summary

    def post_parse(self, result_json):
        pass

    def get_default_image(self, size=400):
        org_image_map = {
            self.USDA: 'usda_logo_{size}.jpg',
            self.FDA: 'fda_logo_{size}.jpg',
        }

        filename = org_image_map[self.organization].format(size=size)

        return static('recalls/{}'.format(filename))

    def get_topic_names(self):
        from .forms import RecallTypeForm
        topics = []
        form_data = {'foodndrug': True }
        form = RecallTypeForm(form_data)
        if form.is_valid():
            topics.extend(form.get_topics())

        return topics


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural='Product Manufacturers'
        ordering = ['name']

    def __unicode__(self):
        return u'{}'.format(self.name)


class ProductCategory(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural='Product Categories'
        ordering = ['name']

    def __unicode__(self):
        return u'{}'.format(self.name)


class ProductRecall(Recall):

    descriptions = models.TextField(blank=True)
    hazards = models.TextField(blank=True)
    countries = models.TextField(blank=True)
    product_categories = models.ManyToManyField('ProductCategory')
    product_manufacturers = models.ManyToManyField('ProductManufacturer')

    default_image_fmt = 'recalls/SB-ConsumerProducts-{}px.jpg'

    def __unicode__(self):
        return u"%s" % self.recall_subject

    def get_absolute_url(self):
        return reverse('product_recall_detail',
                       kwargs={'slug': self.slug,
                               'recall_number': self.recall_number})

    def title(self):
        recall_title = super(ProductRecall, self).title()
        if not recall_title:
            recall_title = u'Recall for {}'.format(self.name)
        return recall_title

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
                self.contact_summary = ' '.join([tag.renderContents() for tag in pot_children]).replace('Report an Incident Involving this Product', '')

                break

        meta_description = soup_obj.find('meta', {'name': 'description'})
        if meta_description:
            self.hazards = meta_description.get('content')

        section_map = {
            "Description": 'descriptions',
            "Remedy": 'corrective_summary',
            "Incidents/Injuries": 'consequence_summary',
        }

        for section, dest in section_map.items():
            parsed = soup_obj.find('h5', text=section).findNext()
            if parsed:
                setattr(self, dest, parsed.renderContents())


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

        # Add product category instances for each one found
        for product_type in result_json['product_types']:
            type_obj, created = ProductCategory.objects.get_or_create(
                name=product_type
            )
            self.product_categories.add(type_obj)

        # same for product manufacturers
        for product_manufacturer in result_json['manufacturers']:
            manufacturer_obj, created = ProductManufacturer.objects.get_or_create(
                name=product_manufacturer
            )
            self.product_manufacturers.add(manufacturer_obj)


        # determine the product recall template version via date
        # Before 10-1-2012 -> version 1
        # After 10-1-2012 -> version 2
        # ConceptDemo -> We ain't interested in no concept demos
        # ^^ is actually a search result link that we can't handle.
        # maybe we should email an admin or stick in a queue to get
        # manually updated.
        if self.recall_url:
            if 'ConceptDemo' in self.recall_url:
                from urlparse import urlsplit
                # need to grab the english url from the results screen
                try:
                    search_results = requests.get(self.recall_url, timeout=10).content
                except requests.exceptions.Timeout:
                    logger.error('Product Recall search results timeout: {}'.format(
                        self.recall_url
                    ))
                else:
                    soup = BeautifulSoup(search_results)
                    link = soup.find(id='LabelDocDetails').find(
                        'a',
                        href=re.compile('^http.*/en/')
                    )

                    self.recall_url = link['href']
                    self.save()

            try:
                product_html = requests.get(self.recall_url, timeout=10).content
            except requests.exceptions.Timeout:
                logger.error('Product Recall timeout url: {}'.format(self.recall_url))
            else:
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
                upc_record, _ = ProductUPC.objects.get_or_create(recall=self,
                                                                 upc=upc)

    def get_topic_names(self):
        from .forms import RecallTypeForm
        topics = []
        form_data = {
            'products': True,
        }

        for manufacturer in self.product_manufacturers.all():
            man_form_data = form_data.copy()
            man_form_data.update({'manufacturer': manufacturer.pk})
            form = RecallTypeForm(man_form_data)
            if form.is_valid():
                topics.extend(form.get_topics())

        for category in self.product_categories.all():
            cat_form_data = form_data.copy()
            cat_form_data.update({'product_category': category.pk})
            form = RecallTypeForm(cat_form_data)
            if form.is_valid():
                topics.extend(form.get_topics())

        # get cartesian product of manufacturers and categories

        return topics


class ProductUPC(models.Model):
    recall = models.ForeignKey('ProductRecall')
    upc = models.CharField(_('UPC'), max_length=64, blank=True)


class CarRecall(Recall):
    code = models.CharField(_('code'), max_length=1)

    default_image_fmt = 'recalls/SB-MotorVehicles-{}px.jpg'

    def __unicode__(self):
        return u"%s" % self.recall_subject

    def get_absolute_url(self):
        return reverse('car_recall_detail',
                       kwargs={'slug': self.slug,
                               'recall_number': self.recall_number})

    def post_parse(self, result_json):
        for record_json in result_json['records']:
            record_json.update(recall=self)
            make_str = record_json.pop('make').capitalize()
            try:
                make = CarMake.objects.get(name__iexact=make_str)
            except CarMake.DoesNotExist:
                make = CarMake.objects.create(name=make_str)

            record_json['vehicle_make'] = make

            car_record, _ = CarRecallRecord.objects.get_or_create(
                recalled_component_id=record_json['recalled_component_id'],
                defaults=record_json
            )

    def makes(self):
        return ', '.join(set([record.vehicle_make.name for record in self.carrecallrecord_set.all()]))

    def models(self):
        return ', '.join(set([record.model for record in self.carrecallrecord_set.all()]))

    def years(self):
        return ', '.join(set([str(record.year) for record in self.carrecallrecord_set.all()]))

    def get_image(self, size=400):
        opts = {
            'size': (size, size),
        }

        return self.get_default_image(size=size)

    def should_create_stream_item(self):
        """
        Only create stream items for car recalls that include makes that are
        whitelisted.
        """

        for record in self.carrecallrecord_set.all():
            if record.vehicle_make.show_in_results == True:
                return True

    def get_topic_names(self):
        """ Iterate through `CarRecallRecord` records and return topic names per year. """
        from .forms import RecallTypeForm
        topics = []
        form_data = {'vehicles': True}

        for record in self.carrecallrecord_set.all():
            if record.year and record.model:
                record_form_data = form_data.copy()
                record_form_data.update({
                    'vehicle_year': record.year,
                    'vehicle_model': record.model,
                    'vehicle_make': record.vehicle_make.pk
                })

                form = RecallTypeForm(record_form_data)
                if form.is_valid():
                    topics.extend(form.get_topics())

        return topics

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
    vehicle_make = models.ForeignKey('CarMake', blank=True, null=True)
    model = models.CharField(_('model'), max_length=50, blank=True)

    year = models.PositiveSmallIntegerField(_('year'), max_length=4,
                                            blank=True, null=True)


class CarMake(models.Model):
    name = models.CharField(_('make'), max_length=50)
    logo = models.ImageField(upload_to='assets/recalls/makes',
                             max_length=255, blank=True, null=True)
    show_in_results = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{}'.format(self.name)

    def has_image(self):
        if self.logo:
            return True
        return False
    has_image.boolean = True

    class Meta:
        ordering = ['name']


class CarModel(models.Model):
    make = models.ForeignKey(CarMake)
    name = models.CharField(_('model'), max_length=50)
    years = models.CommaSeparatedIntegerField(max_length=200)

    def __unicode__(self):
        return u'<{}> {}'.format(self.make, self.name)

    class Meta:
        ordering = ['name']


class RecallStreamItem(models.Model):

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    organization = models.PositiveSmallIntegerField(choices=Recall.ORG_CHOICES,
                                                    blank=True, null=True)
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

    image = models.ImageField(upload_to='assets/recalls/images',
                              max_length=255, null=True, blank=True)

    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    def get_image_55(self):
        return self.content_object.get_image_55()

    def get_image_65(self):
        return self.content_object.get_image_65()

    def get_image_90(self):
        return self.content_object.get_image_90()

    def get_image(self):
        return self.content_object.get_image()

    # XXX Template Tag
    def get_default_image_55(self):
        return self.content_object.get_default_image(size=55)

    def get_default_image_65(self):
        return self.content_object.get_default_image(size=65)

    def get_default_image_90(self):
        return self.content_object.get_default_image(size=90)

    def get_default_image_95(self):
        return self.content_object.get_default_image(size=95)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def get_image(self):
        return self.content_object.get_image()

    def title(self):
        return u"%s" % self.content_object


class RecallSNSTopic(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    arn = models.CharField(max_length=100)


class RecallAlert(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    recall = GenericForeignKey('content_type', 'object_id')
    topic = models.ForeignKey(RecallSNSTopic)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)


class ULPublicNotice(models.Model):
    notice_date = models.DateTimeField(blank=True, null=True)
    notice_title = models.CharField(max_length=255)
    notice_link = models.URLField(max_length=255, unique=True)

    class Meta:
        ordering = ['-notice_date']

    def __unicode__(self):
        return u"%s" % self.notice_title


from recalls.signals import create_stream_item, delete_stream_item

for cls in [ProductRecall, FoodRecall, CarRecall]:
    post_save.connect(create_stream_item, sender=cls)
    post_delete.connect(delete_stream_item, sender=cls)
