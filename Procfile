web: gunicorn library.wsgi --log-file -
worker: celery -A library worker --loglevel=info --pool=solo
