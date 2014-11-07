from django import template

from recalls.models import RecallStreamItem

register = template.Library()


@register.assignment_tag(takes_context=True)
def latest_recalls(context, limit=3):
    recalls = RecallStreamItem.objects.order_by('-recall_date', '-pk')[:limit]
    return recalls


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
