import os
import time as t
from datetime import datetime
import time as t
import schedule


def automate():
    os.system("gnome-terminal -e 'bash -c \"./automatebot.sh; exec bash\"'")
    print()
    #os.system("./automatebot.sh")
    
schedule.every(1).hour.do(automate)

while True:
    schedule.run_pending()
    t.sleep(10)
    print('Waiting to update models.')
    