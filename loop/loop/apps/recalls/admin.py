from django.contrib import admin

from recalls.models import CarRecall, ProductRecall, FoodRecall, ProductUPC, CarRecallRecord


for cls in [CarRecall, ProductRecall, FoodRecall, ProductUPC, CarRecallRecord]:
    admin.site.register(cls)
