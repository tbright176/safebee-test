from django.contrib import admin

from suit.admin import SortableStackedInline

from asset_manager.widgets import ImageAssetWidget
from .models import PromoWidget, PromoWidgetItem


class PromoWidgetItemInline(SortableStackedInline):
    raw_id_fields = ('content_item', 'image')
    model = PromoWidgetItem
    extra = 1
    sortable = "order"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "image":
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(PromoWidgetItemInline, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)


class PromoWidgetAdmin(admin.ModelAdmin):
    fields = ('label',)
    inlines = [PromoWidgetItemInline]
    raw_id_fields = ('header_image',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "header_image":
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(PromoWidgetAdmin, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(PromoWidget, PromoWidgetAdmin)
