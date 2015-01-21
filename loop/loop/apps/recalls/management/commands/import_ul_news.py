import feedparser

from dateutil.parser import parse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recalls.models import ULPublicNotice


class Command(BaseCommand):
    help = "Imports UL public notices from settings.UL_NEWS_FEED"

    def handle(self, *args, **kwargs):
        feed = feedparser.parse(settings.UL_NEWS_FEED)
        for entry in feed.entries:
            title = entry.title.split('(')[0].strip()
            link = entry.link
            pub_date = parse(entry.published)
            new_notice, created = ULPublicNotice.objects.update_or_create(
                notice_link=link, defaults={'notice_date': pub_date,
                                            'notice_title': title})
