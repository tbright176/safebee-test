from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class AssetManagerConfig(AppConfig):
    name = 'asset_manager'
    verbose_name = _("Asset Manager")
