import datetime
import requests

from celery import Celery

app = Celery()
app.config_from_object('django.conf:settings')

date = '2014-01-01'

@app.task
def get_recalls(year=datetime.datetime.today().year):
    print "test"
