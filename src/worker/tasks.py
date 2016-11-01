from worker.celery_app import get_celery_app
from common.utils import db_cursor

app = get_celery_app()

"""
CREATE TABLE votes
(
  user_id character varying(100) NOT NULL,
  vote integer,
  last_update timestamp with time zone,
  CONSTRAINT user_id PRIMARY KEY (user_id)
)
"""

@app.task
def process_vote(user_id, update_dt, vote):
    query = """
      INSERT INTO votes(user_id, last_update, vote) VALUES(%(user_id)s, %(update_dt)s, %(vote)s)
      ON CONFLICT(user_id)
      DO UPDATE SET vote = %(vote)s
      WHERE user_id = %(user_id)s
    """

    with db_cursor() as cursor:
        cursor.execute(query, dict(
            user_id=user_id,
            update_dt=update_dt,
            vote=vote
        ))


