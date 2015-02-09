from django import template

from ..models import BuzzStory

register = template.Library()


@register.assignment_tag
def get_buzz_stories(num_stories=8):
    return BuzzStory.activated.all()[:int(num_stories)]
