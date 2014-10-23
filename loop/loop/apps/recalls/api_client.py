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
                    page=1, per_page=10, sort='rel', food_type=None, upc=None):
        """
        Gets recalls from DigitalGov.

        TODO parameter explanation
        """
        params = ''

        resp = requests.get("{url}{params}".format(
            url=self.base_url,
            params=params
        ))

        return resp
