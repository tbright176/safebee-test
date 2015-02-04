from django.core.management.base import BaseCommand

from social.models import SocialStatusRecord


class Command(BaseCommand):

    def handle(self, *args, **options):
        records = SocialStatusRecord.objects.filter(action_completed=False)
        for record in records:
            if record.content_object:
                record.content_object.save()
