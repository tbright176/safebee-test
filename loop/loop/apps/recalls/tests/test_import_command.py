import datetime
import os
import responses

from django.core.management import call_command
from django.test import TestCase

from recalls.api_client import recall_api


class TestImportRecallCommand(TestCase):

    def setUp(self):
        self.api_client = recall_api()

    def stub_import_responses(self):
        responses.add(
            responses.GET,
            '{url}'.format(url=self.api_client.base_url),
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/response_pg1.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.GET,
            '{url}'.format(url=self.api_client.base_url),
            body=open(os.path.join(os.path.dirname(__file__),
                                   'testdata/response_pg2.json'), 'r').read(),
            status=200,
            content_type='application/json'
        )


    @responses.activate
    def test_no_args(self):
        """
        Test that the command tries to import latest recalls.
        """
        self.stub_import_responses()
        call_command('import_recalls')

        import ipdb; ipdb.set_trace()
        self.assertEqual(len(responses.calls), 2)

    def test_date_args(self):
        """
        Test that the command passes start_date and end_date params.
        """
        pass

    def test_since_latest_recall(self):
        """
        Test that the import command will try to import all recalls since
        the last one in the database.
        """
        pass
