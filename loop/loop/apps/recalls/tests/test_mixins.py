from django.views.generic import DetailView
from django.test import TestCase

#from recalls.mixins import LatestRecallsMixin
from .factories import FoodRecallFactory

class ContextView(object):

    def get_context_data(self, **kwargs):
        return {}

# class TestDetailView(LatestRecallsMixin, ContextView):
#     pass

# class TestLatestMixin(TestCase):
#     def setUp(self):
#         recalls = FoodRecallFactory.create_batch(3)
#         view = TestDetailView()
#         self.context = view.get_context_data()

#     def test_latest_context(self):
#         recalls = self.context['latest_recalls']
#         self.assertTrue(recalls[0].recall_date > recalls[1].recall_date)
#         self.assertTrue(recalls[1].recall_date > recalls[2].recall_date)
