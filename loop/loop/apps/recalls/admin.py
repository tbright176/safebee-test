from singlemodeladmin import SingleModelAdmin

from django.contrib import admin

from asset_manager.widgets import ImageAssetWidget
from recalls.models import (CarRecall, ProductRecall, FoodRecall, ProductUPC,
                            CarRecallRecord, CarMake, ProductCategory,
                            ProductManufacturer, CarModel, RecallAlert,
                            RecallSNSTopic, RecallHomePage, RecallStreamItem)


class RecallAdmin(admin.ModelAdmin):
    list_display = ('title', 'recall_date', 'organization')
    list_filter = ('organization',)
    ordering = ['-recall_date']


class CarRecallAdmin(RecallAdmin):
    pass


class ProductRecallAdmin(RecallAdmin):
    pass


class FoodRecallAdmin(RecallAdmin):
    pass


class CarModelInline(admin.TabularInline):
    model = CarModel


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_image', 'show_in_results')
    inlines = [CarModelInline,]


class RecallHomePageAdmin(SingleModelAdmin):
    raw_id_fields = ('featured_recall', 'featured_recall_image')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'featured_recall_image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(RecallHomePageAdmin, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)


class RecallStreamItemAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'recall_date', 'organization',
                    'recall_number')
    list_filter = ('organization',)
    search_fields = ['recall_subject', 'recall_number', 'recall_url',]

    def has_add_permission(self, request):
        return False


admin.site.register(FoodRecall, FoodRecallAdmin)
admin.site.register(ProductRecall, ProductRecallAdmin)
admin.site.register(CarRecall, CarRecallAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductManufacturer)
admin.site.register(RecallAlert)
admin.site.register(RecallSNSTopic)
admin.site.register(RecallHomePage, RecallHomePageAdmin) 
admin.site.register(RecallStreamItem, RecallStreamItemAdmin)
