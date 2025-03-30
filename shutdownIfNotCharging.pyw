from psutil import sensors_battery
from datetime import datetime
from subprocess import run, CREATE_NO_WINDOW
from threading import Thread, Event
from keyboard import wait
from win11toast import toast

checkInterval = 30
stop = Event()

def notify(message,timeout):
    toast(
        "Shut 'er Down",
        message,
        timeout
    )

def stopCallback():
    wait('ctrl+p')
    notify((f"[{str(datetime.now())[:-10]}] Script was manually stopped by user"),2)

    stop.set()

Thread(target=stopCallback, daemon=True).start()

while not stop.is_set():
    if sensors_battery().power_plugged == False:
        notify((f"[{str(datetime.now())[:-10]}] Computer is not charging, shutting down in 3 seconds."),3)
        stop.wait(3)
        run("shutdown -s -f -t 0", shell=True, capture_output=False, creationflags=CREATE_NO_WINDOW)
    stop.wait(checkInterval)

notify((f"[{str(datetime.now())[:-10]}] Script ended cleanly; have a good day sir."),3)