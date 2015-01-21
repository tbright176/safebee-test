from django import template
from django.contrib.contenttypes.models import ContentType

from recalls.models import RecallStreamItem, FoodRecall, Recall, ULPublicNotice

from watson.models import SearchEntry

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

@register.assignment_tag(takes_context=True)
def latest_notices(context, limit=3):
    """
    Return `limit` number of UL public notices, ordered by most recent.
    """
    notices = ULPublicNotice.objects.all()[:limit]
    return notices

@register.assignment_tag
def recall_obj(obj):
    """
    Given either a RecallStreamItem, a SearchResult, or an actual Recall-derived
    class, return the Recall-derived class.
    """
    if isinstance(obj, RecallStreamItem):
        return obj.content_object

    if isinstance(obj, Recall):
        return obj

    if isinstance(obj, SearchEntry):
        return obj.object

    # Prank Caller! Prank Caller
    return obj


@register.assignment_tag
def get_next_recall(current_recall):
    next_item = None
    try:
        next_item = current_recall\
            .get_next_by_recall_date()
    except current_recall.__class__.DoesNotExist:
        pass
    return next_item


@register.assignment_tag
def get_previous_recall(current_recall):
    previous_item = None
    try:
        previous_item = current_recall\
            .get_previous_by_recall_date()
    except current_recall.__class__.DoesNotExist:
        pass
    return previous_item
