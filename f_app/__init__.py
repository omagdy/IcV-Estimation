from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
from f_app import routes
