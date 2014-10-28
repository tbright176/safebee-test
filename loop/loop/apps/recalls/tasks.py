import datetime
import logging
import requests

from celery import Celery

from recalls.api_client import recall_api

app = Celery()
app.config_from_object('django.conf:settings')

logger = logging.getLogger(__name__)

@app.task
def get_recalls(**kwargs):
    """
    A shim of a task to execute recall_api.get_recalls(), passes any kwargs
    to the function.

    returns the number of recalls that have been imported.
    """

    logger.info("Beginning recall import process.")

    recalls = recall_api().import_recalls(**kwargs)

    logger.info("Imported {num_recalls} recalls.".format(
        num_recalls=len(recalls)
    ))

    return len(recalls)
