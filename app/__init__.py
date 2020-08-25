from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from celery import Celery
from celery.utils.log import get_task_logger


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
logger = get_task_logger(__name__)

from app import routes, models