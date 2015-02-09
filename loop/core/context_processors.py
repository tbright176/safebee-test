from django.conf import settings
from django.contrib.sites.models import Site


def site_processor(request):
    return {'current_site': Site.objects.get_current()}


def debug_status(request):
    return {'DEBUG': settings.DEBUG}
