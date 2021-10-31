
import os
import time as t
from datetime import datetime
import time as t
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

print("started automation")

def some_job():
    os.system("gnome-terminal -e 'bash -c \"./automatebot.sh; exec bash\"'")
    print("updated stats at " + str(datetime.datetime.now()))

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()