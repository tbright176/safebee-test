import pytz
from dateutil import parser, tz

from django.core.management.base import BaseCommand
from django.db import transaction

from social.models import DisqusThread
from social.utils.disqus import DisqusAPIClient


class Command(BaseCommand):

    DISQUS_API_HOT_THREADS_KEY = 'DISQUS_API_HOT_THREADS_KEY'
    DISQUS_API_POPULAR_THREADS_KEY = 'DISQUS_API_POPULAR_THREADS_KEY'

    @transaction.atomic
    def handle(self, *args, **options):
        self.disqus = DisqusAPIClient()
        self.hot_threads = []
        self.popular_threads = []
        self.update_hot_threads()
        self.update_popular_threads()

    def update_hot_threads(self):
        results = self.disqus.get_hot_threads()
        if results:
            self.create_threads('H', results)

    def update_popular_threads(self):
        results = self.disqus.get_popular_threads()
        if results:
            self.create_threads('P', results)

    def create_threads(self, thread_type, results):
        old_threads = DisqusThread.objects\
                                  .filter(thread_type=thread_type).delete()
        order = 1
        tz = pytz.timezone('UTC')
        for result in results:
            latest_post = self.disqus.get_latest_post_for_thread(result['id'])
            if latest_post:
                result['createdAt'] = latest_post['createdAt']
            created_at = parser.parse(result['createdAt'])
            created_at = created_at.replace(tzinfo=tz)
            thread = DisqusThread(thread_type=thread_type,
                                  thread_link=result['link'].replace('cms.safebee.com', 'www.safebee.com').replace('?preview=true', ''),
                                  thread_posts=result['posts'],
                                  thread_likes=result['likes'],
                                  thread_title=result['title'],
                                  creation_date=created_at,
                                  order=order)
            thread.save()
            order += 1
