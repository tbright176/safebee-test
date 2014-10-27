import datetime

from django.test import TestCase
from factory import fuzzy
from factory.django import DjangoModelFactory

from recalls.models import Recall, FoodRecall


class RecallFactory(DjangoModelFactory):
    class Meta:
        model = Recall
        abstract = True

    organization = Recall.FDA
    recall_subject = fuzzy.FuzzyText()
    recall_number = fuzzy.FuzzyText()
    recall_url = "http://an.example/url"
    recall_date = fuzzy.FuzzyDate(start_date=datetime.date(1970, 1, 1))

    initiator = "MFR"
    notes = fuzzy.FuzzyText(prefix="Note: ")
    corrective_summary = fuzzy.FuzzyText(prefix="To Fix, ")
    consequence_summary = fuzzy.FuzzyText()
    defect_summary = fuzzy.FuzzyText()


class FoodRecallFactory(RecallFactory):
    class Meta:
        model = FoodRecall

    food_type = FoodRecall.FOOD

class ProductRecallFactory(RecallFactory):
    pass


class CarRecallFactory(RecallFactory):
    report_date = fuzzy.FuzzyDate(start_date=datetime.date(1970, 1, 1))
    year = '2014'
    code = 'A'

class TestRecallABC(TestCase):

    def setUp(self):
        self.recall = FoodRecallFactory()

    def test_recall_type_detection(self):
        pass

    def test_recall_unicode(self):
        """ Make sure both recall_number and recall_subject are in the __unicode__."""
        self.assertIn(self.recall.recall_number, unicode(self.recall))
        self.assertIn(self.recall.recall_subject, unicode(self.recall))
