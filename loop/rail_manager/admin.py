from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect

from suit.admin import SortableStackedInline
from suit_redactor.widgets import RedactorWidget

from .models import Module, Rail, RailItem
from .views import clone_rail
from core.admin import LoopModelAdmin


def clone_rail_action(modeladmin, request, queryset):
    obj_id = queryset[0].id
    return HttpResponseRedirect(reverse("admin:rail_manager_clone_rail_view",
                                        kwargs={"content_id": obj_id}))
clone_rail_action.short_description = "Clone selected rail"


class RailItemInline(SortableStackedInline):
    model = RailItem
    extra = 1
    sortable = "order"


class RailAdmin(LoopModelAdmin):
    actions = [clone_rail_action,]
    inlines = [RailItemInline,]
    list_display = ('title', 'url', 'active')
    list_editable = ['active',]
    save_on_top = True
    search_fields = ['title', 'description']

    def get_urls(self):
        urls = super(RailAdmin, self).get_urls()
        railadmin_urls = patterns('',
            url(r'^clone/(?P<content_id>\d+)/$',
                clone_rail,
                name="rail_manager_clone_rail_view"),
        )
        return railadmin_urls + urls


class ModuleAdmin(LoopModelAdmin):
    list_display = ('title', 'active')
    list_editable = ['active',]
    search_fields = ['title', 'body']

    formfield_overrides = {
        models.TextField: {'widget': RedactorWidget(editor_options=\
                                                    {'minHeight': '300',
                                                     'toolbarFixed': True,
                                                     'toolbarFixedBox': True})},
    }


admin.site.register(Rail, RailAdmin)
admin.site.register(Module, ModuleAdmin)
