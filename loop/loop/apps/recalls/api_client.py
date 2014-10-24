import requests

PER_PAGE = 50


class recall_api(object):

    base_url = 'http://api.usa.gov/recalls/search.json'

    def parse_result(self, result):
        """
        Returns a Recall-derived object that is appropriate for the result that
        is based on the 'organization' field.
        """
        pass

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

        return resp
