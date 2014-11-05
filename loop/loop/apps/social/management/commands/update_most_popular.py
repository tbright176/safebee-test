import os

from django.core.management.base import BaseCommand
from django.core.urlresolvers import resolve
from django.db import transaction

from apiclient.discovery import build

from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage

import httplib2

from core import views as core_views
from social.models import MostPopularItem

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PRIVATE_KEY = FILE_PATH + '/My Project-6ef1d315055a.p12'  # where you store your private key
GSERVICE_EMAIL = '329483338973-b7io4pnsnp290g5boc5jdb114vnvm8pc@developer.gserviceaccount.com'
SITE = 'ga:89363318'  # eg. ga:1234

SCOPE_FEEDS = 'https://www.google.com/analytics/feeds/'
CREDENTIALS_STORE = FILE_PATH + '/credentials.dat'  # credentials cache file


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        self.init()

    def authorize(self, private_key_filename,
                  service_email,
                  scope,
                  credentials_store=CREDENTIALS_STORE):
        """Authorise a service account against Google APIs"""
        http = httplib2.Http()
        storage = Storage(credentials_store)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            key = None
            with open(private_key_filename, 'rb') as f:
                key = f.read()

                credentials = SignedJwtAssertionCredentials(service_email,
                                                            key,
                                                            scope=scope)
                storage.put(credentials)
        else:
            credentials.refresh(http)

        http = credentials.authorize(http)
        return http

    def print_data_table(self, results, trim=False):
        """Given the results from a query, print to screen."""
        if trim:
            format_str = '%25.24s'
        else:
            format_str = '%25s'

        if results.get('rows', []):
            # Print headers.
            output = []
            for header in results.get('columnHeaders'):
                output.append(format_str % header.get('name'))
            print ''.join(output)

            # Print rows.
            for row in results.get('rows'):
                output = []
                for cell in row:
                    output.append(format_str % cell)
                print ''.join(output)
        else:
            print 'No Results Found'

    def print_top_pages(self, service, site, start_date, end_date, max_results=10):
        """Print out top X pages for a given site."""
        query = service.data().ga().get(
            ids=site,
            start_date=start_date,
            end_date=end_date,
            dimensions='ga:hostname,ga:pagePath',
            metrics='ga:pageviews',
            sort='-ga:pageviews',
            filters='ga:hostname!=localhost',
            max_results=max_results).execute()

        self.print_data_table(query)

    def get_top_pages(self, service, site, start_date,
                      end_date, max_results=100):
        """Print out top X pages for a given site."""
        query = service.data().ga().get(
            ids=site,
            start_date=start_date,
            end_date=end_date,
            dimensions='ga:pagePath',
            metrics='ga:pageviews',
            sort='-ga:pageviews',
            filters='ga:hostname!=localhost',
            max_results=max_results).execute()
        return query

    def process_results(self, results):
        if 'rows' in results:
            objs = []
            for row in results['rows']:
                try:
                    view, args, kwargs = resolve(row[0])
                    core_view = getattr(core_views, view.__name__)
                    obj = core_view.model\
                                   .published.filter(basename=kwargs['basename'],
                                                     category__slug=kwargs['category_slug'],
                                                     exclude_from_most_popular=False)
                    if obj:
                        obj = obj[0]
                        if not obj in objs:
                            objs.append(obj)
                except Exception, e:
                    pass
            if objs:
                MostPopularItem.objects.all().delete()
                order = 1
                for obj in objs:
                    item = MostPopularItem(order=order,
                                           title=u"%s" % obj,
                                           link=obj.get_absolute_url())
                    item.save()


    def init(self):
        http = self.authorize(PRIVATE_KEY, GSERVICE_EMAIL, SCOPE_FEEDS)
        service = build(serviceName='analytics', version='v3', http=http)

        # TODO(gmwils): check if service is valid before continuing
        start = 'yesterday'
        end = 'today'
        results = self.get_top_pages(service, SITE, start, end, 100)
        self.process_results(results)
