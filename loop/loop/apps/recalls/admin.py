from django.contrib import admin

from recalls.models import CarRecall, ProductRecall, FoodRecall, ProductUPC, CarRecallRecord, CarMake

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

class CarMakeAdmin(admin.ModelAdmin):

    list_display = ('name', 'has_image', 'show_in_results')


admin.site.register(FoodRecall, FoodRecallAdmin)
admin.site.register(ProductRecall, ProductRecallAdmin)
admin.site.register(CarRecall, CarRecallAdmin)
admin.site.register(CarMake, CarMakeAdmin)
