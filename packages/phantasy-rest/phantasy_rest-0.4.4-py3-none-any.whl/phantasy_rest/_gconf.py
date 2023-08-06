# pass with --config to gunicorn
import multiprocessing
import os
from phantasy_rest._get_conf import default_app_conf as c

MAX_WORKERS = multiprocessing.cpu_count()

# lattice
machine = os.environ.get('PH_MACHINE', c['LATTICE']['MACHINE'])
segment = os.environ.get('PH_SEGMENT', c['LATTICE']['SEGMENT'])

# configurations

bind = os.environ.get('PH_URL', c['GUNICORN']['URL']) + ':' \
        + os.environ.get('PH_PORT', c['GUNICORN']['PORT'])

backlog = int(os.environ.get('PH_BACKLOG', c['GUNICORN']['BACKLOG']))

_n_worker = int(os.environ.get('PH_WORKERS', c['GUNICORN']['WORKERS']))
workers = _n_worker if _n_worker <= MAX_WORKERS else MAX_WORKERS
worker_class = os.environ.get('PH_WORKER_CLASS', c['GUNICORN']['WORKER_CLASS'])
worker_connection = int(os.environ.get('PH_WORKER_CONNECTION', c['GUNICORN']['WORKER_CONNECTION']))
timeout = int(os.environ.get('PH_TIMEOUT', c['GUNICORN']['TIMEOUT']))
keepalive = int(os.environ.get('PH_KEEPALIVE', c['GUNICORN']['KEEPALIVE']))

spew = os.environ.get('PH_SPEW', c['GUNICORN']['SPEW'])

daemon = os.environ.get('PH_DAEMON', c['GUNICORN']['DAEMON'])
pidfile = os.environ.get('PH_PIDFILE', c['GUNICORN']['PIDFILE'])

errorlog = os.environ.get('PH_ERRORLOG', c['GUNICORN']['ERRORLOG'])
loglevel = os.environ.get('PH_LOGLEVEL', c['GUNICORN']['LOGLEVEL'])
accesslog = os.environ.get('PH_ACCESSLOG', c['GUNICORN']['ACCESSLOG'])
access_log_format = os.environ.get('PH_ACCESS_LOG_FORMAT', c['GUNICORN']['ACCESS_LOG_FORMAT'])

## SSL
certfile = os.environ.get('PH_CERTFILE', None)
keyfile = os.environ.get('PH_KEYFILE', None)
