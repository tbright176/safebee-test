from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page, cache_control

from .models import HubPage
from core.models import StreamItem


@cache_control(max_age=settings.CACHE_CONTROL_MAX_AGE)
@cache_page(settings.CACHE_CONTROL_MAX_AGE)
def hubpage(request, hubpage_id, additional_context=None):
    try:
        hubpage = HubPage.objects\
                         .select_related('featured_content',
                                         'featured_content__category',
                                         'featured_content__promo_image',
                                         'featured_content__content_object')\
                         .prefetch_related('hubpagecontentmodule_set',
                                           'hubpagecategorycontentmodule_set')\
                         .get(pk=hubpage_id)
        context = {'hubpage': hubpage}
        if additional_context:
            context.update(additional_context)
        return render(request, 'base.html', context)
    except HubPage.DoesNotExist:
        raise Http404


def home_page(request):
    try:
        homepage = HubPage.objects.get(set_as_homepage=True)
        queryset = StreamItem.published.select_related('category', 'content_type')
        paginator = Paginator(queryset, settings.CORE_DEFAULT_INDEX_LENGTH)
        pagination_obj = None
        try:
            pagination_obj = paginator.page(1)
        except (EmptyPage, InvalidPage):
            raise Http404
        addl_context = {'pagination_obj': pagination_obj,
                        'stream_items': pagination_obj.object_list}
        return hubpage(request, homepage.id, addl_context)
    except HubPage.DoesNotExist:
        raise Http404
