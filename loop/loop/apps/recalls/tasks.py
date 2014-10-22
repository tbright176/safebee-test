import datetime
import requests

from celery import Celery

app = Celery('recalls', broker='django://')

date = '2014-01-01'

@app.task
def get_recalls(year=datetime.datetime.today().year):
    print "test"
