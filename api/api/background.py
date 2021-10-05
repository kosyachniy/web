"""
Background processes
"""

import time
from multiprocessing import Process

from consys.errors import ErrorWrong

from .lib.reports import report
from .models.system import System
from .models.socket import Socket
from .methods.account.disconnect import online_stop


async def reset_online_users(sio):
    """ Reset online users """

    sockets = Socket.get(fields={})

    for socket in sockets:
        await online_stop(sio, socket.id)

def update_server_status():
    """ Update last server time """

    while True:
        try:
            system = System.get('last_server_time')
        except ErrorWrong:
            system = System(id='last_server_time')

        system.data = int(time.time())
        system.save()

        time.sleep(60)


async def background(sio):
    """ Background infinite process """

    # Primary
    ## Reports
    await report.info("Restart server")

    ## Online users
    await reset_online_users(sio)

    # Regular
    ## Update last server time
    process_status = Process(target=update_server_status)
    process_status.start()

    ## Reports
    # process_reports = Process(target=reports_process)
    # process_reports.start()
