python3 manage.py migrate

gunicorn premier_league_api.wsgi --bind 0.0.0.0:8000