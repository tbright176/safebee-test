from core.search_indexes import ContentIndex, SiteIndexMixin

from haystack import indexes

from .models import Image


class ImageIndex(indexes.SearchIndex, SiteIndexMixin, indexes.Indexable):
    """ Index class for Images. """

    text = indexes.CharField(document=True, use_template=True)

    alt_text = indexes.CharField(model_attr='alt_text')
    caption = indexes.CharField(model_attr='caption')
    created_by = indexes.CharField(model_attr='created_by')
    creation_date = indexes.DateTimeField(model_attr='creation_date')
    license = indexes.CharField(model_attr='asset_license__name', null=True)
    url = indexes.CharField(model_attr='get_absolute_url')

    def get_updated_field(self):
        return 'modification_date'

    def get_model(self):
        return Image
