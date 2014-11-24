from django.contrib import admin

from recalls.models import (CarRecall, ProductRecall, FoodRecall, ProductUPC,
                            CarRecallRecord, CarMake, ProductCategory,
                            ProductManufacturer, CarModel)

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


admin.site.register(FoodRecall, FoodRecallAdmin)
admin.site.register(ProductRecall, ProductRecallAdmin)
admin.site.register(CarRecall, CarRecallAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductManufacturer)
