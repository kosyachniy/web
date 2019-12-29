# env/bin/gunicorn app:app --worker-class eventlet -w 1 --bind 0.0.0.0:5000 --reload
# env/bin/gunicorn app:app -c gun.py

worker_class = "eventlet"
workers = 1
# threads = 3
bind = "0.0.0.0:5000"
# keepalive = 120
# timeout = 120
reload = True
# accesslog = "-" # STDOUT
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(q)s" "%(D)s"'
# pidfile = '/tmp/gunicorn.pid'
# debug = True
# loglevel = 'debug'
# errorlog = '/tmp/gunicorn.log'
# daemon = True
