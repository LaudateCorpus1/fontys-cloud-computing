import psycopg2
import os
from contextlib import contextmanager

import requests
from requests.auth import HTTPBasicAuth
from urlparse import urlparse

from decorator import decorator


def run_once(f):
    """Run decorated function only once. Subsequent invocations return the
    result of the first."""
    def _run_once(func, *args, **kwargs):
        if not _run_once._has_run:
            result = func(*args, **kwargs)
            _run_once._has_run = True #has run is True after it has actually run
            _run_once._result = result
            return result
        else:
            return _run_once._result
    _run_once._has_run = False

    decorated_func = decorator(_run_once, f)

    def reset_run_once():
        _run_once._has_run = False
    decorated_func._reset = reset_run_once

    return decorated_func


def get_tasks_in_queue(amqp_url, queue_name='celery'):
    amqp_details = urlparse(amqp_url)
    host = amqp_details.hostname
    username = amqp_details.username
    vhost = amqp_details.path[1:] # First character is a slash...
    password = amqp_details.password

    if host == 'localhost':
        # special case
        url = 'http://{host}:55672/api/queues/{vhost}/{queue_name}'.format(
            host=host, vhost=vhost, queue_name=queue_name)
    else:
        url = 'https://{host}/api/queues/{vhost}/{queue_name}'.format(
            host=host, vhost=vhost, queue_name=queue_name)

    queue = requests.get(
        url,
        auth=HTTPBasicAuth(username, password), verify=True).json()

    return queue['messages'] - queue['messages_unacknowledged']


@contextmanager
def db_cursor():
    result = urlparse(os.environ['DATABASE_URL'])
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        connection.commit()
        connection.close()