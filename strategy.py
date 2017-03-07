# -*- coding: utf-8 -*-
import os
from time import sleep

from Conf import *


def restart_eth_software(conf_path):
    os.system("taskkill -im EthDcrMiner64.exe -f")
    sleep(5)
    os.system('"' + conf_path + '"')


def restart_zec_software(conf_path):
    os.system("taskkill -im ZecMiner64.exe -f")
    sleep(5)
    os.system('"' + conf_path + '"')

strategy_dict = dict()
strategy_dict[ETH] = restart_eth_software
strategy_dict[ZEC] = restart_zec_software

