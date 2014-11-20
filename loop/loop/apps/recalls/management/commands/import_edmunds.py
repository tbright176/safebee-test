import logging
import requests

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from recalls.models import CarMake, CarModel


logger = logging.getLogger('loop.recalls.import')
edmunds_api_endpoint = 'https://api.edmunds.com/api/vehicle/v2/makes?view=basic&fmt=json&api_key=usyasttpz5xddysqxddps823'


class Command(BaseCommand):
    help = "Imports Vehicle Make/Models from Edmunds API"

    option_list = BaseCommand.option_list + (
        make_option('--clear',
                    action='store_true',
                    dest='clear'
                ),
    )

    def handle(self, *args, **kwargs):
        makes_created = 0
        models_created = 0

        if kwargs.get('clear'):
            logger.info('Removing existing Makes/Models')
            for make in CarMake.objects.all():
                make.delete()

        logger.info('Starting Edmunds data import')

        try:
            edmunds_resp = requests.get(edmunds_api_endpoint).json()
        except requests.exceptions.ConnectionError:
            logger.info('Error connecting to Edmunds API')
        except requests.exceptions.Timeout:
            logger.info('Timeout connecting to Edmunds API')
        else:
            for make_json in edmunds_resp.get('makes'):
                logger.info('Importing {}'.format(make_json['name']))
                make, created = CarMake.objects.get_or_create(
                    name=make_json['name'],
                    defaults={'show_in_results': False}
                )

                if created:
                    makes_created += 1

                for model_json in make_json['models']:
                    model, created = CarModel.objects.get_or_create(
                        name=model_json['name'],
                        make=make
                    )

                    if created:
                        models_created += 1

                logger.info('Done.')
            logger.info('Import Complete. Makes imported: {}, Models imported: {}'.format(makes_created, models_created))
