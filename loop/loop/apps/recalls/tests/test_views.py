import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from recalls.tests.factories import ProductRecallFactory, FoodRecallFactory, CarRecallFactory, CarMakeFactory, CarModelFactory


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


class TestRecallSignupAjax(TestCase):

    def setUp(self):
        self.make = CarMakeFactory()

        self.model1 = CarModelFactory(make=self.make)
        self.model2 = CarModelFactory(
            make=self.make,
            years='2001'
        )

        self.other_make = CarMakeFactory()
        self.other_model = CarModelFactory(make=self.other_make, years='1920')

    def test_models_ajax_view(self):
        resp = self.client.get(reverse('recalls_car_models'), {'make_id': self.make.pk})
        models = [model['value'] for model in json.loads(resp.content)]
        self.assertIn(self.model1.name, models)
        self.assertIn(self.model2.name, models)
        self.assertNotIn(self.other_model, models)

    def test_years_ajax_view(self):
        resp = self.client.get(reverse('recalls_car_years'), {'model_id': self.model1.pk})
        years = [year['value'] for year in json.loads(resp.content)]

        self.assertIn(self.model1.years.split(',')[0], years)
        self.assertIn(self.model1.years.split(',')[1], years)
        self.assertNotIn(self.other_model.years, years)
