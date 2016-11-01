import os

from celery import Celery

from common.utils import run_once


class CeleryConfig(object):
    CELERYD_CONCURRENCY = 1
    CELERY_ACKS_LATE = True
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']


@run_once
def get_celery_app():
    app = Celery("Celery", broker=os.environ['AMQP_URL'])
    app.config_from_object(CeleryConfig())
    return app