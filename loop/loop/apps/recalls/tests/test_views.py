from django.core.urlresolvers import reverse
from django.test import TestCase

from recalls.models import ProductRecall
from recalls.tests.factories import ProductRecallFactory


class TestProductDetail(TestCase):

    def setUp(self):
        self.recall = ProductRecallFactory()

    def test_product_detail_view(self):
        response = self.client.get(self.recall.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        recall_attrs = [
            'recall_number',
            'hazards',
            'corrective_summary',
            'descriptions'
        ]
        for prop in recall_attrs:
            self.assertContains(response, getattr(self.recall, prop))
