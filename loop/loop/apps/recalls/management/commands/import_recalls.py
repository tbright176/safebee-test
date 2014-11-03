import datetime
import logging

from dateutil.relativedelta import *
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from recalls.tasks import get_recalls

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Imports recall data from digitalgov.gov"

    option_list = BaseCommand.option_list + (
        make_option('--start_date',
                    action='store',
                    dest='start_date',
                    default=str(datetime.date.today() - relativedelta(months=1))
                ),
        make_option('--end_date',
                    action='store',
                    dest='end_date',
                    default=str(datetime.date.today())
                ),
        make_option('--org',
                    action='store',
                    dest='org',
                ),
    )

    def handle(self, *args, **kwargs):
        org = kwargs.get('org')
        if org:
            kwargs['organizations'] = [org]

        kwargs['sort'] = 'date'


        get_recalls(**kwargs)
        logging.info('Import complete.')
