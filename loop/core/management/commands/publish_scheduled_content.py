from django.utils import timezone

from django.core.management.base import BaseCommand
from core.models import Content


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = timezone.now()
        subclasses = Content.__subclasses__()
        for subclass in subclasses:
            scheduled = subclass.scheduled.all()
            for content_item in scheduled:
                if content_item.publication_date <= now:
                    content_item.status = 'P'
                    content_item.save()
