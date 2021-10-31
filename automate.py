import os
import time as t
from datetime import datetime
import time as t

from apscheduler.schedulers.blocking import BlockingScheduler

def some_job():
    os.system("gnome-terminal -e 'bash -c \"./automatebot.sh; exec bash\"'")

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()