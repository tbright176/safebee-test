import datetime

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
    summary = fuzzy.FuzzyText(prefix="Don't eat, because ")

class ProductRecallFactory(RecallFactory):
    pass


class CarRecallFactory(RecallFactory):
    report_date = fuzzy.FuzzyDate(start_date=datetime.date(1970, 1, 1))
    year = '2014'
    code = 'A'
