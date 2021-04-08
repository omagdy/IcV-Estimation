#!/bin/bash

nohup redis-server &
export PYTHONPATH="$PYTHONPATH:/app/icv/app"
nohup celery -A app.celery worker --loglevel=info &
nohup flask run --host=0.0.0.0 &
