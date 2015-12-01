from django.core import management

from loop.celery_config import app


@app.task
def publish_scheduled_content():
    management.call_command('publish_scheduled_content')
