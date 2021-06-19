"""
Background processes
"""

# Libraries
## System
import time
from multiprocessing import Process

## Local
from .funcs import online_user_update, online_session_close, report
from .funcs.mongodb import db
from .models.socket import Socket


def reset_online_users():
    """ Reset online users """

    sockets = Socket.get(fields={'user'})

    for socket in sockets:
        online_user_update(socket.user)
        online_session_close(socket)

def update_server_status():
    """ Update last server time """

    while True:
        req = int(time.time())

        res = db.sys.update_one(
            {'name': 'last_server_time'},
            {'$set': {'cont': req}}
        )

        if not res.modified_count:
            db.sys.insert_one({'name': 'last_server_time', 'cont': req})

        time.sleep(60)


def background(sio):
    """ Background infinite process """

    # Primary
    ## Reports
    report("Restart server")

    ## Online users
    reset_online_users()

    # Regular
    ## Update last server time
    process_status = Process(target=update_server_status)
    process_status.start()

    ## Reports
    # process_reports = Process(target=reports_process)
    # process_reports.start()
