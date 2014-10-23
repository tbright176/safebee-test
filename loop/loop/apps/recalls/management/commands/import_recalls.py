from django.core.management.base import BaseCommand, CommandError
#from recalls.models import Recall

from recalls.tasks import get_recalls

class Command(BaseCommand):
    help = "Imports recall data from csc"

    def handle(self, *args, **kwargs):
        get_recalls.apply_async()
