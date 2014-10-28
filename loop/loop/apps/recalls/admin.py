from django.contrib import admin

from recalls.models import CarRecall, ProductRecall, FoodRecall, ProductUPC, CarRecallRecord

class RecallAdmin(admin.ModelAdmin):
    pass


class CarRecallAdmin(RecallAdmin):
    pass


class ProductRecallAdmin(RecallAdmin):
    pass


class FoodRecallAdmin(RecallAdmin):
    pass


admin.site.register(FoodRecall, FoodRecallAdmin)
admin.site.register(ProductRecall, ProductRecallAdmin)
admin.site.register(CarRecall, CarRecallAdmin)
