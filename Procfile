web: gunicorn --chdir src flask_app.web_app:app --log-level INFO
worker: celery --workdir=src --app=worker.tasks --loglevel=INFO worker -Ofair -c 1