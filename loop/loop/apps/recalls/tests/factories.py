import datetime

from factory import fuzzy
from factory.django import DjangoModelFactory, ImageField

from recalls.models import Recall, FoodRecall, ProductRecall, CarRecall, CarMake, CarModel


class RecallFactory(DjangoModelFactory):
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
    image = ImageField()

    class Meta:
        model = Recall
        abstract = True


class FoodRecallFactory(RecallFactory):

    food_type = FoodRecall.FOOD
    summary = fuzzy.FuzzyText(prefix="Don't eat, because ")

    class Meta:
        model = FoodRecall


class ProductRecallFactory(RecallFactory):

    class Meta:
        model = ProductRecall


class CarRecallFactory(RecallFactory):

    code = 'A'

    class Meta:
        model = CarRecall

class CarMakeFactory(DjangoModelFactory):

    class Meta:
        model = CarMake

    name = fuzzy.FuzzyText()

class CarModelFactory(DjangoModelFactory):

    class Meta:
        model = CarModel

    make = CarMakeFactory()
