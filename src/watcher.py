import os
import time
import threading
from functions import load_config
from variables import *

file_changed_event = threading.Event()


def config_watcher():
    last_mtime = os.path.getmtime(CONFIG_PATH)

    while True:
        this_mtime = os.path.getmtime(CONFIG_PATH)
        if this_mtime > last_mtime:
            print("File changed")
            load_config()
            file_changed_event.set()
            last_mtime = this_mtime

        time.sleep(3)


def register_config_watcher():
    watcher_thread = threading.Thread(target=config_watcher)
    watcher_thread.start()
    return file_changed_event
