import mock

from django.test import TestCase

from recalls.api_client import recall_api


class TestRecallAPIClient(TestCase):

    def setUp(self):
        self.api_client = recall_api()

    @mock.patch('requests.get')
    def test_client_no_params(self, mock_req):
        """ Make sure that a minimal call to get_recalls() builds a valid url. """

        self.api_client.get_recalls()

        self.assertEqual(mock_req.call_count, 1)
        self.assertEqual(mock_req.call_args[0][0], recall_api.base_url)

    def test_client_query(self):
        pass

    def test_client_organizations(self):
        pass

    def test_client_date_range(self):
        pass

    def test_client_paging(self):
        pass

    def test_client_sorting(self):
        pass

    def test_client_food_type(self):
        pass

    def test_client_upc(self):
        pass

    def test_url_full_params(self):
        pass
