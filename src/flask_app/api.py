import datetime
import os

from flask import Flask
from flask_restful import Resource, Api, reqparse

from flask_app.auth import requires_auth
from worker.tasks import process_vote
from common.utils import get_tasks_in_queue, db_cursor

vote_parser = reqparse.RequestParser()
vote_parser.add_argument('user_id', required=True, location="json")
vote_parser.add_argument('vote', required=True, location="json")


class Vote(Resource):
    def patch(self):
        """Use send a vote"""
        args = vote_parser.parse_args()
        process_vote.delay(
            user_id=args['user_id'],
            vote=args['vote'],
            update_dt=datetime.datetime.utcnow()
        )


class Dashboard(Resource):
    decorators = [requires_auth]

    def get(self):
        with db_cursor() as cursor:
            cursor.execute("""
            SELECT
              SUM(CAST(vote=1 as integer)) as up_votes,
              SUM(CAST(vote=-1 as integer)) as down_votes
            FROM
              votes
            WHERE
              last_update >= NOW() - INTERVAL '15 minutes'
              """)
            votes_up, votes_down = cursor.fetchone()

        status = dict(
            votes_up=votes_up,
            votes_down=votes_down,
            queue_depth=get_tasks_in_queue(os.environ['AMQP_URL'])
        )
        return status


app = Flask(__name__)
api = Api(app)

api.add_resource(Vote, '/vote')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    app.run(debug=True)

