from django.contrib import admin

from suit.admin import SortableStackedInline

from asset_manager.widgets import ImageAssetWidget
from core.admin import LoopModelAdmin, FeaturedItemInline
from .forms import (HubPageAdminForm, HubPageCategoryContentModuleAdminForm,
                    HubPageContentModuleAdminForm)
from .models import (HubPage, HubPageCategoryContentModule,
                     HubPageContentModule, ContentModule, ContentModuleItem,
                     HubPageFeaturedItem)


class ContentModuleItemInline(SortableStackedInline):
    model = ContentModuleItem
    extra = 0
    raw_id_fields = ('content_object', 'content_image',)
    sortable = 'order'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'content_image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(ContentModuleItemInline, self)\
            .formfield_for_foreignkey(db_field,
                                      request,
                                      **kwargs)


class ContentModuleAdmin(LoopModelAdmin):
    inlines = [ContentModuleItemInline,]

    class Media:
        js = ('hubpage/admin/stream_popup.js',)


class HubPageContentModuleInline(SortableStackedInline):
    form = HubPageContentModuleAdminForm
    model = HubPageContentModule
    extra = 0
    sortable = 'order'


class HubPageCategoryContentModuleInline(SortableStackedInline):
    form = HubPageCategoryContentModuleAdminForm
    model = HubPageCategoryContentModule
    exclude = ('display_featured_story_only',)
    extra = 0
    sortable = 'order'


class HubPageFeaturedItemInline(FeaturedItemInline):
    model = HubPageFeaturedItem
    verbose_name = 'Home Page Featured Item'
    verbose_name_plural = 'Home Page Featured Item'


class HubPageAdmin(LoopModelAdmin):
    form = HubPageAdminForm
    inlines = [HubPageFeaturedItemInline,]
    exclude = ('featured_content', 'featured_content_title',
               'featured_content_description', 'featured_content_image',
               'featured_content_url', 'hide_byline')
    raw_id_fields = ('featured_content', 'featured_content_image',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'featured_content_image':
            kwargs['widget'] = ImageAssetWidget()
            return db_field.formfield(**kwargs)
        return super(HubPageAdmin, self).formfield_for_foreignkey(db_field,
                                                                  request,
                                                                  **kwargs)

admin.site.register(HubPage, HubPageAdmin)
