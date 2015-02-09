from django.contrib import admin

from models import BuzzStory


class BuzzStoryAdmin(admin.ModelAdmin):
    list_display = ('stream_item', 'pub_date', 'active')
    list_display_links = None
    list_editable = ('active',)
    search_fields = ('stream_item__title',)

    def pub_date(self, obj):
        return obj.stream_item.publication_date
    pub_date.short_description = 'Publication Date'


admin.site.register(BuzzStory, BuzzStoryAdmin)
