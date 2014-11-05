from django import template
from django.contrib.contenttypes.models import ContentType

from recalls.models import RecallStreamItem, FoodRecall

register = template.Library()


@register.assignment_tag(takes_context=True)
def recalls_and_alerts(context, limit=3):
    """
    Return `limit` number of recall items, ordered by most recent.

    excludes recalls that don't have images.
    """
    food_ct = ContentType.objects.get_for_model(FoodRecall)
    recalls = RecallStreamItem.objects.exclude(content_type=food_ct).exclude(image='').order_by('-recall_date', '-pk')[:limit]
    return recalls

@register.assignment_tag(takes_context=True)
def latest_recalls(context, limit=3):
    """
    Return `limit` number of recall items, ordered by most recent.
    """
    recalls = RecallStreamItem.objects.order_by('-recall_date', '-pk')[:limit]
    return recalls
