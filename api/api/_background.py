"""
Background processes
"""

# Libraries
## System
# import timestamp
# from multiprocessing import Process

## Local
from api._func import report


def background(sio):
    report("Restart server")

    # Primary
    # ## Reset online users
    # for online in db['online'].find():
    #     online_user_update(online)
    #     online_session_close(online)
    #     db['online'].remove(online['_id'])

    # Regular

    # process_reports = Process(target=reports_process)
    # process_reports.start()
