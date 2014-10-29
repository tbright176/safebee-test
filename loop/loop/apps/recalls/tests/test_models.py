from django.test import TestCase

from factories import FoodRecallFactory


class TestRecallABC(TestCase):

    def setUp(self):
        self.recall = FoodRecallFactory()

    def test_recall_type_detection(self):
        pass

    def test_recall_unicode(self):
        """ Make sure that recall_summary is in the __unicode__."""
        self.assertIn(self.recall.summary, unicode(self.recall))
