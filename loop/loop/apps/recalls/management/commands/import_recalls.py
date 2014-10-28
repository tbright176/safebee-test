from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from recalls.tasks import get_recalls


class Command(BaseCommand):
    help = "Imports recall data from digitalgov.gov"

    option_list = BaseCommand.option_list + (
        make_option('--start_date',
                    action='store_true',
                    dest='start_date',
                    default=False,
                ),
        make_option('--end_date',
                    action='store_true',
                    dest='end_date',
                    default=False,
                ),
        make_option('--org',
                    action='store',
                    dest='org',
                    default=False,
                ),
    )

    def handle(self, *args, **kwargs):
        params = {}
        org = kwargs.get('org')
        if org:
            params['organizations'] = [org]

        get_recalls.apply_async(kwargs=params)
        self.stdout.write('Import complete.')
