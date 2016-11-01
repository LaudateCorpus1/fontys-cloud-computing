import os

from celery import Celery

from common.utils import run_once


@run_once
def get_celery_app():
    return Celery("Celery", broker=os.environ['AMQP_URL'])