# -*- coding: utf-8 -*-
""""
    File name: mythread.py
    Author: amazing
    Date last modified: 3/28/2017
    Python Version: 3.5
"""

import threading
from time import sleep


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self.stop_flag = threading.Event()

    def stop(self):
        self.stop_flag.set()

    def stopped(self):
        return self.stop_flag.isSet()

    def run(self):
        while True:
            print('test')
            sleep(3)
            if self.stopped():
                break

