#!/bin/bash

nohup flask run --host=0.0.0.0 &
nohup redis-server &
nohup celery -A app.celery worker --loglevel=info &
