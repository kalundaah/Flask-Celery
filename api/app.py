import os
from flask import Flask
from api.celery_config import celery_init_app
from api import create_app

app = create_app()
celery_app = app.extensions["celery"]

# Accessing a specific queue
# celery -A api.app.celery_app worker -Q example --loglevel=INFO

# remote control
# celery -A api.app.celery_app inspect active

# celery control : force workers to enable event messages
# celery -A api.app.celery_app control enable_events

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, threaded=True)


