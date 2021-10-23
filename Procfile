release: python manage.py migrate
web: gunicorn danker_man.wsgi
celery: celery -A danker_man worker -l INFO
