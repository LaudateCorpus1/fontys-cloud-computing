from werkzeug.wsgi import DispatcherMiddleware

from flask_app.api import app as api_app
from flask_app.static_app import app as static_app

app = DispatcherMiddleware(api_app, {
    '/app':     static_app
})