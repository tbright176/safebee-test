from django.core import management

from loop.celery import app


@app.task
def update_disqus():
    management.call_command('update_disqus')

@app.task
def update_most_popular():
    management.call_command('update_most_popular')

@app.task
def retry_social_service_action():
    management.call_command('retry_social_service_action')
