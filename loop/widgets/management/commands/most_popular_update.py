import requests

from urlparse import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.urlresolvers import resolve
from django.db.models import F

from core import views as core_views
from core.models import StreamItem
from widgets.models import PromoWidget, PromoWidgetItem


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.limit = 5
        self.widget, created = PromoWidget.objects.get_or_create(label="Most Popular")
        api_url = '%s?apikey=%s&host=%s&limit=%s'\
                  % (settings.CHARTBEAT_API_URL,
                     settings.CHARTBEAT_API_KEY,
                     settings.CHARTBEAT_API_HOST,
                     50)
        response = requests.get(api_url)
        if response.ok:
            content_objects = self.get_content_objects(response.json())
            stream_items = self.get_stream_items(content_objects)

            # bump order of existing items to ensure any renderings of
            # this widget still have data while we're updating it
            self.widget.promowidgetitem_set.update(order=F('order') + 500)

            widget_items = self.get_widget_items(stream_items)
            if widget_items:
                # delete any beyond the limit...
                self.widget.promowidgetitem_set.filter(order__gte=self.limit).delete()

    def get_widget_items(self, stream_items):
        widget_items = []
        order = 0
        for item in stream_items:
            widget_item, created = PromoWidgetItem.objects.get_or_create(widget=self.widget, content_item=item, order=order)
            widget_items.append(widget_item)
            order += 1
        return widget_items

    def get_stream_items(self, content_objects):
        items = []
        for obj in content_objects:
            c_type = ContentType.objects.get_for_model(obj)
            try:
                item = StreamItem.published.get(object_id=obj.id,
                                                content_type=c_type)
                items.append(item)
            except StreamItem.DoesNotExist:
                continue
        return items

    def get_content_objects(self, resp_json):
        objs = []
        urls = [page['path'] for page in resp_json['pages']]
        for url in urls:
            parsed = urlparse(url)
            try:
                view, args, kwargs = resolve(parsed.path.replace(settings.CHARTBEAT_API_HOST, ''))
                core_view = getattr(core_views, view.__name__)
                obj = core_view.model\
                               .published.filter(basename=kwargs['basename'],
                                                 category__slug=kwargs['category_slug'],
                                                 exclude_from_most_popular=False)
                if obj:
                    obj = obj[0]
                    objs.append(obj)
            except Exception, e:
                #print parsed.path, ": ", e
                pass

        return objs
