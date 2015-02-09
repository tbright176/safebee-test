from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class RailManagerConfig(AppConfig):
    name = 'loop.rail_manager'
    verbose_name = _("Rail Manager")
