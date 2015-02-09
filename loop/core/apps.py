from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = 'loop.core'
    verbose_name = _("Content")
