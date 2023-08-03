#!/bin/sh

# in Alpine Linux the cron deamon is not running by default
crond

python manage.py crontab remove
python manage.py crontab add
python manage.py crontab show

python manage.py runserver 0.0.0.0:8000
