import requests
import pickle
from celery import shared_task, task
from celery.task.control import inspect
from .models import AdInfo



@shared_task
def ads_update_runner():
    pass