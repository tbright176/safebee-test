import requests

from collections import defaultdict

from django import template
from django.conf import settings
from django.contrib.sites.models import Site

from social.models import DisqusThread, MostPopularItem, MostPopularRecall

register = template.Library()


@register.assignment_tag(takes_context=True)
def disqus_popular_threads(context, limit=3):
    return DisqusThread.objects.filter(thread_type='P')[:limit]


@register.assignment_tag(takes_context=True)
def disqus_hot_threads(context, limit=3):
    return DisqusThread.objects.filter(thread_type='H')[:limit]


@register.assignment_tag(takes_context=True)
def most_popular_items(context, limit=10):
    return MostPopularItem.objects.all()[:limit]


@register.assignment_tag(takes_context=True)
def most_popular_recalls(context, limit=10):
    return MostPopularRecall.objects.all()[:limit]


@register.assignment_tag(takes_context=True)
def social_counts(context, url):
    """
    Retrieve social counts for the given URL from the SharedCount API.

    Defaultdict is used to provide a count of 0 for any arbitrary key, which
    allows us to skip setting up a default dict with keys reflecting the various
    social services in favor of simply taking whatever SharedCount returns.

    In the case of Facebook, since the value of the key is a dictionary itself,
    we use the 'total_count' value as the count for the service.

    Example API response:

    {
        'StumbleUpon': 0,
        'Reddit': 0,
        'Delicious': 0,
        'Pinterest': 0,
        'Twitter': 0,
        'Diggs': 0,
        'LinkedIn': 0,
        'Facebook': {
            'commentsbox_count': 0,
            'click_count': 0,
            'total_count': 0,
            'comment_count': 0,
            'like_count': 0,
            'share_count': 0
        },
        'GooglePlusOne': 0,
        'Buzz': 0
    }
    """
    if not url.find('http://') == 0:
        url = "http://%s%s" % (Site.objects.get_current().domain, url)
    counts = defaultdict(int)
    api_url = "%s?url=%s&apikey=%s" % (settings.SHAREDCOUNT_API_ENDPOINT,
                                       url,
                                       settings.SHAREDCOUNT_API_KEY)
    aggregate_count = 0

    if settings.SHAREDCOUNT_ENABLED:
        resp = requests.get(api_url)
        if resp.status_code == requests.codes.ok:
            resp_json = resp.json()
            for service, service_count in resp_json.items():
                service_name = service.lower()
                if not service_name == 'facebook':
                    counts[service_name] = service_count
                else:
                    counts[service_name] = service_count['total_count']
                aggregate_count += counts[service_name]
            for service, count in counts.items():
                if count < settings.SHAREDCOUNT_DISPLAY_LOWER_LIMIT:
                    counts[service] = 0
    counts['aggregate_count'] = aggregate_count
    return counts
