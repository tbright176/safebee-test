import requests

from collections import defaultdict

from django import template
from django.conf import settings

register = template.Library()


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
    counts = defaultdict(int)
    api_url = "%s?url=%s&apikey=%s" % (settings.SHAREDCOUNT_API_ENDPOINT,
                                       url,
                                       settings.SHAREDCOUNT_API_KEY)

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
            for service, count in counts.items():
                if count < settings.SHAREDCOUNT_DISPLAY_LOWER_LIMIT:
                    counts[service] = 0

    return counts
