from celery import shared_task, task
from celery.task.control import inspect


@shared_task
def ad_checker():
    pass