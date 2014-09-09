import humanize
import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from easy_thumbnails.files import get_thumbnailer

from .models import Image


def image_data(request):
    image_id = request.GET.get('image_id', None)
    if not image_id:
        raise Http404
    image = get_object_or_404(Image, pk=image_id)
    thumbnail = get_thumbnailer(image.asset)['admin_change_list']
    image_info = {
        'image_width': image.asset.width,
        'image_height': image.asset.height,
        'image_size': humanize.naturalsize(image.asset.size),
        'image_caption': image.caption,
        'thumbnail_url': thumbnail.url,
    }
    data = json.dumps(image_info)
    return HttpResponse(data, content_type='application/json')

def widget_with_value(request):
    image_id = request.GET.get('image_id', None)
    if not image_id:
        raise Http404
    image = get_object_or_404(Image, pk=image_id)
    thumbnail = get_thumbnailer(image.asset)['admin_change_list']
    image_info = {
        'image_width': image.asset.width,
        'image_height': image.asset.height,
        'image_size': humanize.naturalsize(image.asset.size),
        'image_caption': image.caption,
        'thumbnail_url': thumbnail.url,
        'change_url': reverse('admin:asset_manager_image_changelist'),
        'name': request.GET.get('name', None),
        'value': image_id,
    }
    output = render_to_string('widget_with_value.html', image_info)
    return HttpResponse(mark_safe(output))

def image_html_snippet(request):
    image_id = request.GET.get('image_id', None)
    if not image_id:
        raise Http404
    image = get_object_or_404(Image, pk=image_id)
    thumbnail = get_thumbnailer(image.asset)['default_content_well']
    image_info = {
        'image_alt_text': image.alt_text,
        'image_width': image.asset.width,
        'image_height': image.asset.height,
        'image_size': humanize.naturalsize(image.asset.size),
        'image_caption': image.caption,
        'thumbnail_url': thumbnail.url,
        'asset': image,
    }
    return render(request, 'body_html_insert.html', image_info)
