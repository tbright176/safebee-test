from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class FlatPagesConfig(AppConfig):
    name = 'loop.flatpages'
    verbose_name = _("Flat Pages")
