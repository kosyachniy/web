"""
Background processes
"""

# Libraries
## System
import time
from multiprocessing import Process

## Local
from .funcs import online_stop, report
from .funcs.mongodb import db
from .models.socket import Socket


async def reset_online_users(sio):
    """ Reset online users """

    sockets = Socket.get(fields={})

    for socket in sockets:
        await online_stop(sio, socket.id)

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


async def background(sio):
    """ Background infinite process """

    # Primary
    ## Reports
    report.info("Restart server", path='background.background')

    ## Online users
    await reset_online_users(sio)

    # Regular
    ## Update last server time
    process_status = Process(target=update_server_status)
    process_status.start()

    ## Reports
    # process_reports = Process(target=reports_process)
    # process_reports.start()
