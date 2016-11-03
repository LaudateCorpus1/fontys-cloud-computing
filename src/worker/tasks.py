import logging
import time
import os

from worker.celery_app import get_celery_app
from common.utils import db_cursor
from celery.utils.log import get_task_logger

app = get_celery_app()

logger = get_task_logger(__name__)

task_delay = int(os.environ.get('TASK_DELAY', '0'))

"""
CREATE TABLE votes
(
  user_id character varying(100) NOT NULL,
  vote integer,
  last_update timestamp with time zone,
  count integer;
  CONSTRAINT user_id PRIMARY KEY (user_id)
)
"""

@app.task
def process_vote(user_id, update_dt, vote):

    # Simulate heavy processing
    time.sleep(task_delay / 1000.0)

    query = """
      INSERT INTO votes(user_id, last_update, vote) VALUES(%(user_id)s, %(update_dt)s, %(vote)s)
      ON CONFLICT(user_id)
      DO UPDATE SET (vote, last_update) = (%(vote)s, %(update_dt)s)
      WHERE votes.user_id = %(user_id)s
    """

    count_query = """
      UPDATE votes
      SET count = count+1
      WHERE user_id = %(user_id)s
    """

    with db_cursor() as cursor:
        cursor.execute(query, dict(
            user_id=user_id,
            update_dt=update_dt,
            vote=vote
        ))
        cursor.execute(count_query, dict(user_id=user_id))


