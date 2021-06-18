"""
Background processes
"""

# Libraries
## System
# import timestamp
# from multiprocessing import Process

## Local
from .funcs import report
from .funcs import online_user_update, online_session_close
from .models.socket import Socket


def reset_online_users():
    """ Reset online users """

    sockets = Socket.get(fields={'user'})

    for socket in sockets:
        online_user_update(socket.user)
        online_session_close(socket)


def background(sio):
    """ Background infinite process """

    # Primary
    ## Reports
    report("Restart server")

    ## Online users
    reset_online_users()

    # Regular
    # ## Reports
    # process_reports = Process(target=reports_process)
    # process_reports.start()
