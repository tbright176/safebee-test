from django import template

from recalls.models import RecallStreamItem

register = template.Library()


@register.assignment_tag(takes_context=True)
def latest_recalls(context, limit=3):
    recalls = RecallStreamItem.objects.order_by('-recall_date', '-pk')[:limit]
    return recalls
