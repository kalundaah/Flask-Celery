import os
from flask import Flask
from api.celery_config import celery_init_app
from api.routes import tasks,primitives

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Flask_Celery.sqlite'),
        CELERY = dict(
            broker_url = os.getenv("BROKER_URL"),
            result_backend = os.getenv("BACKEND_URL"),
            task_ignore_result = True,
            task_serializer = 'json',
            result_serializer = 'json',
            accept_content = ['json'],
            timezone = 'Africa/Nairobi',
            enable_utc = True,
            task_routes = {'tasks.add':{'rate_limit':'10/m'}},
            result_expires=3600,
        ),
        DEVELOPMENT = True,
        FLASK_DEBUG = True,
        TESTING = True,
        DEBUG = True,
        SEND_FILE_MAX_AGE_DEFAULT = 300,
        TIMEOUT= 90
    )
    app.config.from_prefixed_env()
    celery_init_app(app=app)
    
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(primitives, url_prefix="/primitives")
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
