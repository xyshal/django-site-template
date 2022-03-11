import multiprocessing
import os

wsgi_app = "testsite.wsgi:application"

env_log = os.environ.get('GUNICORN_LOGLEVEL')
loglevel = env_log if env_log != None else "info"

reload = os.environ.get('GUNICORN_DEBUG') == "True"

workers = multiprocessing.cpu_count() * 2
bind = "0.0.0.0:8000"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = True
pidfile = "/var/log/gunicorn/gunicorn.pid"
