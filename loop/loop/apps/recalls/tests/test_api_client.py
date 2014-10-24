import datetime
import mock
import os
import responses
import urllib

from django.test import TestCase

from recalls.api_client import recall_api
from recalls.models import FoodRecall, CarRecall, ProductRecall


class TestRecallAPIParser(TestCase):

    @responses.activate
    def setUp(self):
        self.api_client = recall_api()
        self.stub_responses()

        self.api_client.get_recalls()

    def stub_responses(self):
        responses.add(
            responses.GET,
            self.api_client.base_url,
            body=open(os.path.join(os.path.dirname(__file__), 'testdata/all_types.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )

    def test_parse_food_types(self):
        """
        Test that the various food types are imported properly.
        """
        self.assertEqual(FoodRecall.objects.count(), 2)

    def test_parse_car(self):
        """
        Test that multiple records are imported properly, also make a separate
        model for those w/ relationship.
        """
        self.assertEqual(CarRecall.objects.count(), 1)

    def test_parse_product_types(self):
        """
        Test that product recalls are parsed properly.
        """
        # TODO make sure upc=null doesn't break anything.
        self.assertEqual(ProductRecall.objects.count(), 2)


class TestRecallAPIClient(TestCase):

    def setUp(self):
        self.api_client = recall_api()

    def stub_responses(self):
        responses.add(
            responses.GET,
            self.api_client.base_url,
            body='{"success": "stuff"}',
            status=200,
            content_type='application/json'
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

        self.assertEqual(responses.calls[0].request.url, recall_api.base_url)

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
        self.assertIn(org, responses.calls[0].request.url)

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
        sort = 'date'

        self.api_client.get_recalls(sort=sort)
        self.assertIn("sort={}".format(sort), responses.calls[0].request.url)

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
