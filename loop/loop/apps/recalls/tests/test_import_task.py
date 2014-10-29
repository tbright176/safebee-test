import os
import responses

from mock import patch

from django.test import TestCase

from recalls.models import ProductRecall
from recalls.tasks import get_recalls
from recalls.api_client import recall_api
# some tests for the import task, such as does it iterate through multiple results 'pages', do date ranges work, etc

class TestImportRecallTask(TestCase):

    def setUp(self):
        pass

    @patch.object(recall_api, 'import_recalls')
    def test_task_kwargs(self, mock_method):
        """
        Make sure kwargs are passed directly to the function import recalls
        function.
        """

        kwargs = {
            'kwarg1': 'value1',
            'kwarg2': 'value2'
        }

        get_recalls(**kwargs)
        mock_method.assert_called_with(**kwargs)
