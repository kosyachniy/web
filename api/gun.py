from sets import SERVER


worker_class = 'eventlet'
workers = 1
# threads = 3
bind = '{}:{}'.format(SERVER['ip'], SERVER['port'])
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
