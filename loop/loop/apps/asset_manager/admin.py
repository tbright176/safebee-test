import copy

from django.conf.urls import url
from django.contrib import admin

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from core.admin import LoopModelAdmin
from .models import Image
from .views import image_data, image_html_snippet, widget_with_value


class AssetAdmin(LoopModelAdmin):
    default_fieldsets = [
        ('Assets', {
            'fields': ('asset',),
        }),
        ('General', {
            'fields': ('caption', 'display_caption',)
        }),
        ('Attribution', {
            'fields': ('asset_author', 'asset_source', 'asset_organization',
                       'asset_organization_source', 'asset_license',)
        }),
        ('Other', {
            'fields': ('notes', 'created_by', 'creation_date',
                       'modification_date',)
        })
    ]
    list_display = ('caption', 'created_by', 'creation_date',)
    readonly_fields = ('created_by', 'creation_date', 'modification_date',)
    search_fields = ['caption', 'notes']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            fieldsets = copy.deepcopy(self.default_fieldsets)
            for fieldset in fieldsets:
                if fieldset[0] == 'Other':
                    fieldset[1]['fields'] = [field for field\
                                             in fieldset[1]['fields']\
                                             if not field\
                                             in self.readonly_fields]
            return fieldsets
        return self.default_fieldsets

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

    class Media:
        css = {
            'all': ('asset_manager/admin/input.css',)
        }


class ImageAdmin(AssetAdmin):
    list_per_page = 50

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ImageAdmin, self).get_fieldsets(request, obj)
        for fieldset in fieldsets:
            if fieldset[0] == 'Assets':
                fieldset[1]['fields'] = ('asset', 'social_asset',
                                         'promo_asset')
            if fieldset[0] == 'General':
                fieldset[1]['fields'] = ('caption', 'display_caption',
                                         'alt_text')
        return fieldsets

    def get_list_display(self, request):
        return ('show_thumbnail', 'caption', 'alt_text',
                'created_by', 'creation_date',)

    def get_urls(self):
        urls = super(ImageAdmin, self).get_urls()
        added_urls = [
            url(r'image_info/$', self.admin_site.admin_view(image_data),
                name='asset_manager_image_info'),
            url(r'image_html_snippet/$',
                self.admin_site.admin_view(image_html_snippet),
                name='asset_manager_image_html_snippet'),
            url(r'widget_with_value/$',
                self.admin_site.admin_view(widget_with_value),
                name='asset_manager_widget_with_value'),
        ]
        return added_urls + urls

    def show_thumbnail(self, obj):
        if obj.asset:
            try:
                thumb = get_thumbnailer(obj.asset)['admin_change_list']
                return u"""<img src="%s" />""" % thumb.url
            except InvalidImageFormatError:
                pass
        return u''
    show_thumbnail.short_description = "Thumbnail"
    show_thumbnail.allow_tags = True

admin.site.register(Image, ImageAdmin)
