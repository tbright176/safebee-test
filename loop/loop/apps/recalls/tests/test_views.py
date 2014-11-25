from django.core.urlresolvers import reverse
from django.test import TestCase

from recalls.tests.factories import ProductRecallFactory, FoodRecallFactory, CarRecallFactory


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


class TestIndexViews(TestCase):

    def setUp(self):
        pass

    def test_recall_index_page(self):
        recalls = FoodRecallFactory.create_batch(5)
        resp = self.client.get(reverse('recalls_list'))
        self.assertEqual(resp.context['category_title'], 'All Recalls')

    def test_product_index_page(self):
        recalls = ProductRecallFactory.create_batch(5)
        resp = self.client.get(reverse('product_recall_list'))
        self.assertEqual(resp.context['category_title'], 'Consumer Products')

    def test_food_index_page(self):
        recalls = FoodRecallFactory.create_batch(5)
        resp = self.client.get(reverse('food_recall_list'))
        self.assertEqual(resp.context['category_title'], 'Food & Drugs')

    def test_car_index_page(self):
        recalls = CarRecallFactory.create_batch(5)
        resp = self.client.get(reverse('car_recall_list'))
        self.assertEqual(resp.context['category_title'], 'Motor Vehicles')

class TestRecallSignup(TestCase):

    def setUp(self):
        pass

    def test_get_topic(self):
        pass
