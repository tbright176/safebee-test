from suit.admin import SortableStackedInline

from django.contrib import admin

from asset_manager.widgets import ImageAssetWidget
from core.admin import ContentAdmin
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
    inlines = [
        FeaturedItemInline,
    ]


admin.site.register(Feature, FeatureAdmin)
