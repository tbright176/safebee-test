from django.core.management.base import BaseCommand, CommandError

from recalls.tasks import get_recalls


class Command(BaseCommand):
    help = "Imports recall data from digitalgov.gov"

    def handle(self, *args, **kwargs):
        get_recalls.apply_async()
        self.stdout.write('Import complete.')
