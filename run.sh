#!/bin/bash

nohup python manage.py celery beat > celery-beat.log 2>&1 &
nohup python manage.py celery worker --loglevel=info --settings=blogproject.settings > celery-worker.log 2>&1 &

