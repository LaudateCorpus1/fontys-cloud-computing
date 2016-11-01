import os

from celery import Celery

from common.utils import run_once


@run_once
def get_celery_app():
    app = Celery("Celery", broker=os.environ['AMQP_URL'])
    #
    # CELERY_ACKS_LATE = True
    # CELERYD_PREFETCH_MULTIPLIER = 1
    #
    # app.config_from_object()
    return app