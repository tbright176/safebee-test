from django.test import TestCase

from .factories import FoodRecallFactory, ProductRecallFactory, CarRecallFactory
from recalls.models import RecallStreamItem, CarRecall, ProductRecall, FoodRecall


class TestRecallABC(TestCase):

    def setUp(self):
        self.recall = FoodRecallFactory()

    def test_recall_type_detection(self):
        pass

    def test_recall_unicode(self):
        """ Make sure that recall_summary is in the __unicode__."""
        self.assertIn(self.recall.summary, unicode(self.recall))

class TestRecallStream(TestCase):

    def setUp(self):
        self.food_recalls = FoodRecallFactory.create_batch(2)
        self.product_recalls = ProductRecallFactory.create_batch(2)
        self.car_recalls = CarRecallFactory.create_batch(2)

    def total_recalls(self):
        return sum([
            CarRecall.objects.count(),
            ProductRecall.objects.count(),
            FoodRecall.objects.count()
        ])

    def test_recall_stream(self):
        """ Make sure the Recall Stream is built properly. """
        self.assertEqual(RecallStreamItem.objects.count(), self.total_recalls())

    def test_recall_stream_delete(self):
        """
        Make sure that deleting a couple objects deletes their corresponding stream
        items.
        """

        for obj in self.car_recalls:
            obj.delete()

        self.assertEqual(RecallStreamItem.objects.count(), self.total_recalls())
