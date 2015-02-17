import copy

from suit.admin import SortableStackedInline

from django.contrib import admin

from asset_manager.widgets import ImageAssetWidget
from core.admin import ContentAdmin

from .forms import FeatureAdminForm
from .models import Feature, FeaturedItem


class FeaturedItemInline(SortableStackedInline):
    model = FeaturedItem
    extra = 0
    raw_id_fields = ('image', 'content_item')

    class Media:
        js = ('core/admin/related_stream_popup.js',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(FeaturedItemInline, self).formfield_for_foreignkey(db_field,
                                                                        request,
                                                                        **kwargs)


class FeatureAdmin(ContentAdmin):
    form = FeatureAdminForm
    inlines = [
        FeaturedItemInline,
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(FeatureAdmin, self).get_fieldsets(request, obj)
        fieldsets_copy = copy.deepcopy(fieldsets)
        if len(fieldsets_copy) > 2:
            if not fieldsets_copy[1][0] == 'Intro Copy':
                body_fieldset = ('Intro Copy', {
                    'classes': ('full-width', 'wide',
                                'suit-tab suit-tab-general'),
                    'fields': ('intro_copy',)
                })
                fieldsets_copy.insert(1, body_fieldset)
        return fieldsets_copy


admin.site.register(Feature, FeatureAdmin)
