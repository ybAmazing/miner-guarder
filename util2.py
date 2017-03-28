# -*- coding: utf-8 -*-
""""
    File name: util2.py
    Author: amazing
    Date last modified: 3/28/2017
    Python Version: 3.5
"""

import socket
import threading
from time import sleep

from Conf import *


def get_address_worker(file_path):
    with open(file_path) as f:
        for line in f:
            if line.startswith("EthDcrMiner64.exe"):
                words = line.split()
                wallet = words[words.index("-ewal") + 1]
                name = words[words.index("-eworker") + 1]
                return [wallet, name]
            if line.startswith("ZecMiner64.exe"):
                pass


def make_id(pool, coin, address, worker):
    if coin == ETH:
        address = address.lower()
    if address.startswith("0x") or address.startswith("0X"):
        address = address[2:]
    return " ".join((address, pool, coin, worker))


def make_id_from_file(file_path, pool_type, coin_type):
    if coin_type == ETH:
        return make_eth_id_from_file(file_path, pool_type)
    if coin_type == ZEC:
        return make_zec_id_from_file(file_path, pool_type)


def make_eth_id_from_file(file_path, pool_type):
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("EthDcrMiner64.exe"):
                words = line.split()
                address = words[words.index("-ewal") + 1]
                address = address.lower()
                name = words[words.index("-eworker") + 1]
                return make_id(pool_type, ETH, address, name)


def make_zec_id_from_file(file_path, pool_type):
    with open("./config.txt") as f:
        content = f.read()
        words = content.split()
        address_name = words[words.index("-zwal")+1]
        [address, name] = address_name.split(".")
        return make_id(pool_type, ZEC, address, name)


def heart_beat(id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            while True:
                try:
                    s.sendall(id)
                    cmd = s.recv(1024)
                    if not cmd:
                        s.close()
                        break
                    if cmd == '1':
                        t = threading.Thread(target=close_open_machine, args=(self.bat_path,))
                        t.start()
                except:
                    pass
                sleep(TIME_SPAN)
        except:
            sleep(TIME_SPAN)
            pass
    s.close()
