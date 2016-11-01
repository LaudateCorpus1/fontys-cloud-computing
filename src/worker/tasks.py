from worker.celery_app import get_celery_app
from common.utils import db_cursor

app = get_celery_app()


@app.task
def process_vote(user_id, update_dt, vote):
    query = """
      INSERT INTO votes(user_id, last_update, vote) VALUES(%s, %s, %s)
      ON CONFLICT(user_id)
      DO UPDATE SET vote=%s
      WHERE user_id = %s
    """

    with db_cursor() as cursor:
        cursor.execute(query)


