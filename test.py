# import winreg

# key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Minerhelper")
# # newKey = winreg.CreateKey(key, "Minerhelper")
# # winreg.SetValue(newKey, "conf_path",  winreg.REG_SZ, "test")
#
# value = winreg.QueryValue(key, "conf_path")
# print(value)

# try:
#     i = 0
#     while 1:
#       name, value, type= winreg.EnumValue(key, i)
#       print(repr(name))
#       i += 1
# except WindowsError:
#     print()

# from mythread import StoppableThread
# from time import sleep
#
#
# def func():
#     while True:
#         print('haha')
#         sleep(3)
#
#
# stop_thread = StoppableThread()
# stop_thread.start()
# sleep(10)
# stop_thread.stop()
# stop_thread.join()

import socket
from Conf import *
from time import sleep

# from hbthread import HeartBeatThread
#
#
# t = HeartBeatThread('hahaha', 'test', 'ETH')
# t.start()

import winreg

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Minerhelper")
winreg.DeleteKey(key, "coin_type")
winreg.DeleteKey(key, "pool_type")
winreg.DeleteKey(key, "conf_path")





