import requests

PER_PAGE = 50

from models import FoodRecall, CarRecall, CarRecallRecord, ProductRecall, Recall, ProductUPC


class RecallParameterException(Exception):
    pass


class recall_api(object):

    base_url = 'http://api.usa.gov/recalls/search.json'

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

        obj_cls, org = org_cls_mapping[result['organization']]
        obj_data = {}

        for field in obj_cls._meta.fields:
            if result.has_key(field.name):
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

        if obj_cls == ProductRecall and result['upcs']:
            for upc in result['upcs']:
                upc_record, _ = ProductUPC.objects.get_or_create(recall=recall_obj, upc=upc)

        return recall_obj

    def get_recalls(self, query=None, organizations=[], start_date=None, end_date=None,
                    page=None, per_page=None, sort=None, food_type=None, upc=None):
        """
        Gets recalls from DigitalGov.

        TODO parameter explanation
        """
        params = {
            'query': query,
            'sort': sort,
            'upc': upc,
            'food_type': food_type,
            'page': page,
            'per_page': per_page,
            'start_date': start_date,
            'end_date': end_date,
            'organizations': organizations
        }

        resp = requests.get("{url}".format(url=self.base_url), params=params)
        response_json = resp.json()

        pre_results = response_json['success']['results']
        results = []

        for result in pre_results:
            results.append(self.parse_result(result))

        return results
