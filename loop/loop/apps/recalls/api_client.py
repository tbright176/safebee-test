import logging
import requests

from BeautifulSoup import BeautifulSoup

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from models import (FoodRecall, CarRecall, CarRecallRecord, ProductRecall,
                    Recall, ProductUPC)

PAGE_SIZE = 50
MAX_PAGES = 20

BS_KWARGS = {
    'convertEntities': BeautifulSoup.HTML_ENTITIES
}

logger = logging.getLogger(__name__)


class RecallParameterException(Exception):
    pass


class recall_api(object):

    base_url = 'http://api.usa.gov/recalls/search.json'

    def __init__(self, page_size=PAGE_SIZE):
        self.page_size = page_size

    def parse_result(self, result):
        """
        Returns a Recall-derived object that is appropriate for the result that
        is based on the 'organization' field.

        This specifically requires the json `result` have a
        'organization' and 'recall_number'.

        """
        org_cls_mapping = {
            'CPSC': (ProductRecall, Recall.CPSC),
            'FDA': (FoodRecall, Recall.FDA),
            'NHTSA': (CarRecall, Recall.NHTSA),
            'USDA': (FoodRecall, Recall.USDA)
        }

        # some fields are lists, combine these
        list_fields = [
            'manufacturers',
            'product_types',
            'descriptions',
            'hazards',
            'countries',
        ]

        obj_cls, org = org_cls_mapping[result['organization']]
        obj_data = {}

        for field in obj_cls._meta.fields:
            if result.has_key(field.name):
                if field.name in list_fields:
                    obj_data[field.name] = ', '.join(result[field.name])
                else:
                    obj_data[field.name] = result[field.name]

        obj_data['organization'] = org
        recall_obj, created = obj_cls.objects.get_or_create(recall_number=result['recall_number'],
                                                            defaults=obj_data)

        if obj_cls == CarRecall:
            for record_json in result['records']:
                record_json.update(recall=recall_obj)
                car_record, _ = CarRecallRecord.objects.get_or_create(
                    recalled_component_id=record_json['recalled_component_id'],
                    defaults=record_json
                )

        if obj_cls == ProductRecall:
            if result['recall_url']:
                product_html = requests.get(obj_data['recall_url']).content
                soup = BeautifulSoup(product_html, **BS_KWARGS)
                page_images = soup.findAll('img')

                # the first and last images are header/footer images
                # everything else inbetween are product images
                if len(page_images) > 2: # header+footer images
                    image_url = page_images[1].get('src')
                    response = requests.get('http://cpsc.gov{}'.format(image_url))
                    if response.status_code == 200:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(response.content)
                        img_temp.flush()
                        recall_obj.image.save(response.request.url.split('/')[-1],
                                              File(img_temp), save=True)
                    else:
                        logger.error('Non 200 while trying to retrieve: {}'.format(image_url))

            if result['upcs']:
                for upc in result['upcs']:
                    upc_record, _ = ProductUPC.objects.get_or_create(recall=recall_obj, upc=upc)

        return recall_obj, created

    def get_recalls(self, query=None, organizations=[], start_date=None, end_date=None,
                    page=1, per_page=None, sort=None, food_type=None, upc=None, **kwargs):
        """
        Gets recalls from DigitalGov.

        Returns the newly-created results and a boolean denoting if there are
        more results

        TODO parameter explanation
        """

        page_size = per_page or self.page_size
        params = {
            'query': query,
            'sort': sort,
            'upc': upc,
            'food_type': food_type,
            'page': page,
            'per_page': page_size,
            'start_date': start_date,
            'end_date': end_date,
            'organization': organizations
        }

        resp = requests.get("{url}".format(url=self.base_url), params=params)
        response_json = resp.json()
        pre_results = response_json['success']['results']
        total_recalls = response_json['success']['total']

        # sauce: http://bit.ly/1sG8wPd
        # calculates the last page based on the total number of results and the
        # currently-used page size
        last_page = -(-total_recalls // page_size)
        # TIL upside-down floor division

        results = []

        for result in pre_results:
            parsed, created = self.parse_result(result)
            if created:
                results.append(parsed)

        return (results, page < last_page)

    def import_recalls(self, **kwargs):
        """
        Import entry point that handles pagination.
        """

        more = True
        page = 1
        num_results = 0

        while more and page <= MAX_PAGES:
            results, more = self.get_recalls(page=page, **kwargs)
            num_results += len(results)
            page += 1
