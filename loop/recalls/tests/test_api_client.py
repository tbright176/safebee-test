import datetime
import os
import re
import responses
import urllib

from django.test import TestCase

from recalls.api_client import recall_api, PAGE_SIZE
from recalls.models import (FoodRecall, CarRecall, ProductRecall,
                            CarRecallRecord, ProductCategory, ProductManufacturer)

from .factories import CarMakeFactory

class TestRecallAPIParser(TestCase):

    @responses.activate
    def setUp(self):

        self.car_make = CarMakeFactory(name='Spartan')

        self.api_client = recall_api()
        self.stub_responses()
        self.api_client.get_recalls()

    def stub_responses(self):
        old_product_detail = re.compile('http://www.cpsc.gov/cpscpub/prerel/\w+/\w+.html')
        new_product_detail = re.compile('http://www.cpsc.gov/en/Recalls/\d+/.+/')
        product_search_url = re.compile('http://cs.cpsc.gov/ConceptDemo/SearchCPSC.aspx')
        product_image_url = re.compile('http://.+\.jpg')
        fda_spanish_url = re.compile('http://www.fda.gov/Safety/Recalls/ucm431620.htm')
        fda_english_url = re.compile('http://www.fda.gov/Safety/Recalls/ucm216371.htm')

        cpsc_service = (
            (self.api_client.base_url, 'testdata/all_types.json'),
            (old_product_detail, 'testdata/product_detail.html'),
            (new_product_detail, 'testdata/product_detail_new.html'),
            (product_search_url, 'testdata/product_search_url.html'),
            (product_image_url, 'testdata/product_image.jpg'),
            (fda_spanish_url, 'testdata/en_espanol.html'),
            (fda_english_url, 'testdata/in_english.html'),
            ('http://placehold.it/500x500', 'testdata/product_image.jpg')
        )

        for url, file in cpsc_service:
            responses.add(
                responses.GET,
                url,
                body=open(os.path.join(os.path.dirname(__file__), file), 'r').read(),
                status=200
            )

    def test_parse_food_recall(self):
        """
        Test that the various food types are imported properly.
        """

        self.assertEqual(FoodRecall.objects.count(), 2)
        food_recall = FoodRecall.objects.get(recall_number='51d9096a25')

        self.assertEqual(food_recall.organization, FoodRecall.FDA)
        self.assertIn('Listeria monocytogenes', food_recall.description)
        self.assertIn('Lobster Claw and Knuckle Meat', food_recall.summary)

    def test_parse_car_recall(self):
        """
        Test that multiple records are imported properly, also make a separate
        model for those w/ relationship.
        """
        self.assertEqual(CarRecall.objects.count(), 1)
        car_recall = CarRecall.objects.get(recall_number='12V579000')
        car_record = CarRecallRecord.objects.get(recall=car_recall,
                                                 recalled_component_id='000051813001317776000001349')

        self.assertEqual(car_recall.code, 'V')
        self.assertEqual(car_record.component_description, 'VISIBILITY/WIPER')
        self.assertEqual(car_record.manufacturer, 'Spartan Chassis, Inc.')
        self.assertEqual(car_record.manufacturing_begin_date, datetime.date(2012, 10, 1))
        self.assertEqual(car_record.year, 2012)

        self.assertIsNotNone(car_record.vehicle_make)
        self.assertEqual(car_record.vehicle_make, self.car_make)


    def test_parse_old_product_version(self):
        """
        Prior to October 1st, 2012, there was an 'old' version of the product
        detail page that we scape for information.
        """
        self.assertEqual(ProductRecall.objects.count(), 3)

        upc_recall = ProductRecall.objects.get(recall_number='12080')
        sans_upc_recall = ProductRecall.objects.get(recall_number='15016')

        self.assertEqual(upc_recall.recall_number, '12080')
        self.assertEqual(upc_recall.recall_date, datetime.date(2012, 1, 5))
        self.assertEqual(upc_recall.recall_url, 'http://www.cpsc.gov/cpscpub/prerel/prhtml12/12080.html')
        self.assertIn('6-pc. LED Flashlight', upc_recall.descriptions)
        self.assertEqual(upc_recall.hazards, 'Fire & Fire-Related Burn')
        self.assertEqual(upc_recall.countries, 'China')
        self.assertEqual(upc_recall.productupc_set.count(), 1)
        self.assertIn('contact Sterno toll-free', upc_recall.contact_summary)
        self.assertIn('Stop using these candles immediately', upc_recall.corrective_summary)
        self.assertIn('Sterno Recalls Tea Lights', upc_recall.recall_subject)
        self.assertIsNotNone(upc_recall.image.file)

        self.assertEqual(sans_upc_recall.productupc_set.count(), 0)

    def test_parse_product_types(self):
        """
        Test that product types are correctly parsed.
        """

        self.assertEqual(ProductCategory.objects.count(), 4)

        recall1 = ProductRecall.objects.get(recall_number='123')
        recall2 = ProductRecall.objects.get(recall_number='15016')

        self.assertEqual(recall1.product_categories.count(), 2)
        self.assertEqual(recall2.product_categories.count(), 1)

        product_type = recall2.product_categories.first()

        self.assertEqual(product_type.name, 'Telephones, Cell Phones & Accessories')

    def test_parse_product_manufacturers(self):
        """
        Test that product manufacturers are correctly parsed.
        """

        self.assertEqual(ProductManufacturer.objects.count(), 3)

        recall_singular = ProductRecall.objects.get(recall_number='15016')
        recall_plural = ProductRecall.objects.get(recall_number='12080')

        self.assertEqual(recall_singular.product_manufacturers.count(), 1)
        self.assertEqual(recall_plural.product_manufacturers.count(), 2)

        target = ProductManufacturer.objects.get(name='Target')
        tectron = ProductManufacturer.objects.get(name='Tectron International')

        self.assertIn(tectron, recall_singular.product_manufacturers.all())
        self.assertIn(target, recall_plural.product_manufacturers.all())

    def test_parse_new_product_version(self):
        """
        Test that current product detail page parses.

        Starting on October 1st, 2012, there came into existence a new version
        of the product detail page that we scrape for information. For reasons
        that are still unknown to this author, existing product detail pages
        were not converted to the new format.
        """
        recall = ProductRecall.objects.get(recall_number='15016')

        self.assertIn('toll free at (844) 582-3152', recall.contact_summary)
        self.assertIn('Recalls USB Chargers Due to', recall.recall_subject)
        self.assertIn('comes in a transparent sealed pouch.', recall.descriptions)
        self.assertIn('crappy usb charger', recall.corrective_summary)
        self.assertIn('USB charger melting', recall.consequence_summary)
        self.assertIn('posing a fire hazard', recall.hazards)
        self.assertIsNotNone(recall.image.file)

    def test_parse_product_search_results_url(self):
        """
        Test that product search urls are parsed properly.

        Sometimes, products that have multiple product urls instead return a
        search url that gives all of the product detail urls as results.

        When this occurs, we should look for and use the /en/ link to
        retrieve details.
        """

        recall = ProductRecall.objects.get(recall_number='123')
        self.assertEqual(recall.recall_date, datetime.date(2014, 10, 30))
        self.assertEqual(
            recall.recall_url,
            'http://www.cpsc.gov/en/Recalls/2015/Sanus-Simplicity-Television-Wall-Mounts-Recalled-by-Milestone-AV-Technologies/')

class TestRecallAPIClient(TestCase):

    def setUp(self):
        self.api_client = recall_api()
        self.per_page = 10

    def stub_responses(self):
        responses.add(
            responses.GET,
            self.api_client.base_url,
            body='{"success": { "results": [], "total": 0 } }',
            status=200,
            content_type='application/json'
        )

    def stub_paginated_responses(self):
        responses.add(
            responses.GET,
            '{url}?page=1&per_page={per_page}'.format(
                url=self.api_client.base_url,
                per_page=self.per_page
            ),
            match_querystring=True,
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/response_pg1.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.GET,
            '{url}?page=2&per_page={per_page}'.format(
                url=self.api_client.base_url,
                per_page=self.per_page
            ),
            match_querystring=True,
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/response_pg2.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.GET,
            'http://placehold.it/500x500',
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/product_image.jpg'), 'r').read(),
            status=200
        )

    def assertQuotedIn(self, term, url):
        """
        Asserts that the provided `term` is quoted and present in the url.
        """
        return self.assertIn(urllib.quote_plus(term), url)

    @responses.activate
    def test_client_no_params(self):
        """ Make sure that a minimal call to get_recalls() builds a valid url. """
        self.stub_responses()
        self.api_client.get_recalls()

        self.assertEqual(responses.calls[0].request.url,
                         '{}?page=1&per_page={}'.format(
                             recall_api.base_url,
                             PAGE_SIZE
                         )
        )

    @responses.activate
    def test_client_query(self):
        """ Test that a query can be specified in the query. """
        self.stub_responses()
        term = "sonic screwdriver"

        req = self.api_client.get_recalls(query=term)
        self.assertQuotedIn(term, responses.calls[0].request.url)

    @responses.activate
    def test_client_organizations(self):
        """ Test that multiple organizations can be added to the query. """
        self.stub_responses()
        org = "USDA"
        org2 = "FDA"

        self.api_client.get_recalls(organizations=[org])
        self.assertIn("organization={}".format(org), responses.calls[0].request.url)

        self.api_client.get_recalls(organizations=[org, org2])
        self.assertIn(org, responses.calls[1].request.url)
        self.assertIn(org2, responses.calls[1].request.url)

    @responses.activate
    def test_client_date_range(self):
        """ Test that date range parameters are included. """
        self.stub_responses()
        start_date = datetime.date(2014, 10, 1)
        end_date = datetime.date(2014, 12, 31)

        self.api_client.get_recalls(start_date=start_date, end_date=end_date)
        self.assertIn("start_date={}".format(start_date), responses.calls[0].request.url)
        self.assertIn("end_date={}".format(end_date), responses.calls[0].request.url)

    @responses.activate
    def test_client_paging(self):
        """ Test that per_page and page parameters are included correctly. """
        self.stub_responses()
        page = 2
        per_page = 20

        self.api_client.get_recalls(page=page, per_page=per_page)
        self.assertIn("page={}".format(page), responses.calls[0].request.url)
        self.assertIn("per_page={}".format(per_page), responses.calls[0].request.url)

    @responses.activate
    def test_client_sorting(self):
        """
        Test that get_recalls takes sort parameter, validates that it is either
        'rel' or 'date'.

        TODO return RecallParameterException if something other than 'rel' or 'date' is passed.
        """
        self.stub_responses()

        self.api_client.get_recalls()
        self.assertNotIn('sort', responses.calls[0].request.url)

        self.api_client.get_recalls(sort='rel')
        self.assertIn('sort=rel', responses.calls[1].request.url)

    @responses.activate
    def test_client_food_type(self):
        """
        Test that food type parameter is handled correctly.

        TODO RecallParameterException if something other than 'food' or 'drug'
        """
        self.stub_responses()
        food_type = 'drug'

        self.api_client.get_recalls(food_type=food_type)
        self.assertIn("food_type={}".format(food_type), responses.calls[0].request.url)

    @responses.activate
    def test_client_upc(self):
        """
        Test that UPC is valid and passed to the api request.

        TODO if not a valid UPC, RecallParameterException
        """
        self.stub_responses()
        upc = '123'

        self.api_client.get_recalls(upc=upc)
        self.assertIn("upc={}".format(upc), responses.calls[0].request.url)

    @responses.activate
    def test_import_results(self):
        """
        Test that client tries to grab results from multiple pages.
        """

        self.stub_paginated_responses()
        self.api_client.import_recalls(per_page=self.per_page)

        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_product_image_retrieval(self):
        """
        Test that the product parser calls a image retrieval subtask, and that
        it requests the correct page.

        """
        responses.add(
            responses.GET,
            self.api_client.base_url,
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/one_product.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )

        responses.add(
            responses.GET,
            'http://www.cpsc.gov/cpscpub/prerel/prhtml12/12710.html',
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/product_detail.html'), 'r').read(),
            status=200,
            content_type='application/json'
        )

        responses.add(
            responses.GET,
            'http://cpsc.gov/PageFiles/76988/12710.jpg',
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/product_image.jpg'), 'r').read(),
            status=200,
        )

        self.api_client.import_recalls()
        self.assertEqual(ProductRecall.objects.count(), 1)

        recall = ProductRecall.objects.all()[0]

        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(recall.image.height, 240)
