import datetime
import logging
import requests

from django.core import management

from loop.celery_config import app

from recalls.api_client import recall_api

logger = logging.getLogger('loop.recalls.tasks')

@app.task
def get_recalls(**kwargs):
    """
    A shim of a task to execute recall_api.get_recalls(), passes any kwargs
    to the function.
    """

    logger.info("Beginning recall import process.")
    recall_api().import_recalls(**kwargs)

@app.task
def import_recalls():
    management.call_command('import_recalls')

@app.task
def import_ul_news():
    management.call_command('import_ul_news')
