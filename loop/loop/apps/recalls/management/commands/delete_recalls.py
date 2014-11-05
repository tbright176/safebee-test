import datetime
import logging

from dateutil.relativedelta import *
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from recalls.models import FoodRecall, CarRecall, ProductRecall


class Command(BaseCommand):
    help = "Deletes all recalls"

    def handle(self, *args, **kwargs):
        for cls in [FoodRecall, CarRecall, ProductRecall]:
            [obj.delete() for obj in cls.objects.all()]

        print "recalls removed."
