# -*- coding: utf-8 -*-
""""
    File name: hbthread.py
    Author: amazing
    Date last modified: 3/28/2017
    Python Version: 3.5
"""

import threading
from time import sleep
import socket
import os

from Conf import *
from strategy import strategy_dict


def reboot_os():
    os.system("shutdown -t 0 -r -f")


class HeartBeatThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, worker_id, conf_path, coin_type):
        super(HeartBeatThread, self).__init__()
        self.stop_flag = False
        self.worker_id = worker_id
        self.conf_path = conf_path
        self.coin_type = coin_type

    def stop(self):
        self.stop_flag = True

    def stopped(self):
        return self.stop_flag

    def run(self):
        while True:
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((HOST, PORT))
                while True:
                    try:
                        if self.stopped():
                            try:
                                conn.close()
                            except:
                                pass
                            return
                        conn.sendall(self.worker_id.encode())
                        # print("send" + self.worker_id)
                        cmd = conn.recv(1024)
                        cmd = cmd.decode("utf-8")
                        # print(cmd)
                        if not cmd:
                            conn.close()
                            break
                        if cmd == '1':
                            t = threading.Thread(target=strategy_dict[self.coin_type], args=(self.conf_path,))
                            t.start()
                        if cmd == '2':
                            t = threading.Thread(target=reboot_os)
                            t.start()
                    except:
                        pass
                    sleep(TIME_SPAN)
            except:
                sleep(TIME_SPAN)
                pass


