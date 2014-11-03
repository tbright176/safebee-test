from django import template

from recalls.models import ProductRecall

register = template.Library()


@register.assignment_tag(takes_context=True)
def latest_recalls(context, limit=3):
    recalls = ProductRecall.objects.all()[:limit]
    return recalls
