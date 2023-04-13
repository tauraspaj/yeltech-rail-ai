from common import paths
import os

bind = "0.0.0.0:8296"

accesslog = os.path.join(paths.ROOT_DIR, 'logs', 'gunicorn_access.log')
errorlog = os.path.join(paths.ROOT_DIR, 'logs', 'gunicorn_error.log')
capture_output = True
access_log_format = (
    "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s "
    "'%(f)s' '%(a)s' in %(M)sms"
)

workers = int(1)
threads = int(1)

reload = bool(False)
