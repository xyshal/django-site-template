import multiprocessing

wsgi_app = "testsite.wsgi:application"
loglevel = "info"
workers = multiprocessing.cpu_count() * 2
bind = "0.0.0.0:8000"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = True
pidfile = "/var/log/gunicorn/gunicorn.pid"
