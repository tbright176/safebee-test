import humanize

from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from easy_thumbnails.files import get_thumbnailer

from asset_manager.models import Image


class ImageAssetWidget(forms.widgets.TextInput):

    class Media:
        js = ('asset_manager/admin/imageinfo.js',)

    def render(self, name, value, attrs=None):
        if not value or value == 'None':
            value = None
        context = {'name': name, 'value': value or '',
                   'change_url': reverse('admin:asset_manager_image_changelist')}
        if value:
            image = Image.objects.get(pk=int(value))
            thumbnail = get_thumbnailer(image.asset)['admin_change_list']
            context.update({
                'image_id': "%d" % image.pk,
                'thumbnail_url': thumbnail.url,
                'image_width': image.asset.width,
                'image_height': image.asset.height,
                'image_size': humanize.naturalsize(image.asset.size),
                'image_caption': image.caption,
            })

        output = render_to_string('widget.html', context)
        return mark_safe(output)

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + '_id'

    def value_from_datadict(self, data, files, name):
        checkbox_name = self.clear_checkbox_name(name)
        if checkbox_name in data:
            if name in data:
                data[name] = None
        return data.get(name, None)
