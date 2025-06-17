import os
from api import create_app
# from tasks.long_task import test

# celery_app.tasks.register(test())

# Accessing a specific queue
# celery -A api.app.celery_app worker -Q example --loglevel=INFO

# remote control
# celery -A api.app.celery_app inspect active

# celery control : force workers to enable event messages
# celery -A api.app.celery_app control enable_events

application = create_app()
celery_app = application.extensions["celery"]

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    application.run(host=host, port=port, threaded=True)


