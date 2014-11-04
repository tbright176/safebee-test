from django import template

from social.models import DisqusThread

register = template.Library()


@register.assignment_tag(takes_context=True)
def disqus_popular_threads(context, limit=3):
    return DisqusThread.objects.filter(thread_type='P')[:limit]


@register.assignment_tag(takes_context=True)
def disqus_hot_threads(context, limit=3):
    return DisqusThread.objects.filter(thread_type='H')[:limit]
