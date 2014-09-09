from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)

default_app_config = 'asset_manager.apps.AssetManagerConfig'
