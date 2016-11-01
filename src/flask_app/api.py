import datetime
import os

from flask import Flask
from flask_restful import Resource, Api, reqparse

from flask_app.auth import requires_auth
from worker.tasks import process_vote
from common.utils import get_tasks_in_queue

vote_parser = reqparse.RequestParser()
vote_parser.add_argument('user_id', required=True, location="json")
vote_parser.add_argument('vote', type=bool, required=True, location="json")


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
        status = dict(
            votes_up=1,
            votes_down=1,
            queue_depth=get_tasks_in_queue(os.environ['AMQP_URL'])
        )
        return status


app = Flask(__name__)
api = Api(app)

api.add_resource(Vote, '/vote')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    app.run(debug=True)

