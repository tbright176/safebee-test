from suit_redactor.widgets import RedactorWidget

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.admin import LoopModelAdmin
from core.admin_forms import EDITOR_OPTIONS_NO_PLUGINS
from flatpages.forms import FlatpageForm
from flatpages.models import FlatPage


class FlatPageAdmin(LoopModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'description', 'content', 'sites'),
        }),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )
    formfield_overrides = {
        models.TextField: {'widget':\
                           RedactorWidget(editor_options=\
                                          {'minHeight': '300',
                                           'toolbarFixed': True,
                                           'toolbarFixedBox': True,
                                           'convertDivs': False,})},
    }
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')

    class Media:
        css = {
            'all': ('flatpages/admin/input.css',)
        }


admin.site.register(FlatPage, FlatPageAdmin)
