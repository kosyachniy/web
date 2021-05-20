"""
Background processes
"""

# Libraries
## System
# import timestamp
# from multiprocessing import Process

## Local
from api._func import report
from api._func.mongodb import db
from api._func import online_user_update, online_session_close


def reset_online_users():
    """ Reset online users """

    for online in db['online'].find():
        online_user_update(online)
        online_session_close(online)


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
