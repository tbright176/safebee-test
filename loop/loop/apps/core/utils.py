import unicodedata
import sys

from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from .models import Category, LoopUser


def get_author_from_slug(author_slug):
    users = LoopUser.objects.all()
    for user in users:
        if author_slug == slugify(user.get_full_name()):
            return user


def get_categories(category_slug, sub_category_slug=None):
    """
    This is geared towards easing the selection of either a category or
    sub-category as the 'primary' category, given one or two slugs. If a
    sub-category slug is provided, we use both slugs to ensure we get the
    correct sub-category, as we may end up with multiple categories of the
    same name but belonging to different taxonomy trees.

    If a sub-category is found, then it will be returned as the
    primary_category and it's parent as the parent_category. Otherwise, the
    primary category will be for the category_slug provided and the
    parent_category will be None.
    """
    primary_category = None
    parent_category = None
    if sub_category_slug:
        primary_category = Category.objects.select_related('parent')\
                                           .get(slug=sub_category_slug,
                                                parent__slug=category_slug)
        parent_category = primary_category.parent
    else:
        primary_category = Category.objects.select_related('parent')\
                                           .get(slug=category_slug)

    return primary_category, parent_category


def strip_punctuation(text):
    """
    Strip punctuation characters from unicode strings.
    """
    table = dict.fromkeys(i for i in xrange(sys.maxunicode)
                          if unicodedata.category(unichr(i)).startswith('P'))
    return text.translate(table)


def get_streamitem_from_obj(obj):
    """
    Return the Stream Item associated with `obj` if exists
    """

    from .models import StreamItem

    ct = ContentType.objects.get_for_model(obj)

    try:
        return StreamItem.objects.get(
            content_type=ct,
            object_id=obj.pk
        )
    except StreamItem.DoesNotExist:
        return None