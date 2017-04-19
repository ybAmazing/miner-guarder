# -*- coding: utf-8 -*-
""""
    File name: main2.py
    Author: amazing
    Date last modified: 3/28/2017
    Python Version: 3.5
"""

import sys
import os
# from PyQt4 import QtGui, uic
# from PyQt4.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui, Qt
from PyQt5.QtWidgets import *
import winreg
from hbthread import HeartBeatThread
from regedit_helper import prepend_env

from util2 import *

if len(sys.argv) > 1:
    work_path = sys.argv[1]
    os.chdir(work_path)

qtCreatorFile = "./main.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, conf_path=None, pool_type=None, coin_type=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("矿机助手V2.0")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.Qt.WindowMaximizeButtonHint)

        pool_list = [F2POOL, ETHFANS, WATERHOLE]
        coin_list = [ETH, ZEC]
        self.pool_type_list.addItems(pool_list)
        self.coin_type_list.addItems(coin_list)
        self.conf_btn.clicked.connect(self.select_file_path)
        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)
        self.heart_beat_thread = None
        self.conf_path.setWordWrap(True)

        # Check if it is self-starting
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\Windows\CurrentVersion\Run")
            winreg.QueryValueEx(key, "miner_helper")
        except FileNotFoundError:
            self.auto_run_check.setChecked(False)
        else:
            self.auto_run_check.setChecked(True)
        self.auto_run_check.stateChanged.connect(self.auto_run_change)

        if conf_path is not None and coin_type is not None and pool_type is not None:
            try:
                worker_id = make_id_from_file(conf_path, pool_type, coin_type)
            except:
                return

            self.conf_path.setText(conf_path)
            self.pool_type_list.setCurrentIndex(POOL2INDEX[pool_type])
            self.pool_type_list.setEnabled(False)
            self.coin_type_list.setCurrentIndex(COIN2INDEX[coin_type])
            self.coin_type_list.setEnabled(False)
            self.conf_btn.setEnabled(False)
            self.run_btn.setEnabled(False)

            os.chdir(os.path.dirname(conf_path))
            self.heart_beat_thread = HeartBeatThread(worker_id, conf_path, coin_type)
            self.heart_beat_thread.daemon = True
            self.heart_beat_thread.start()

    def select_file_path(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilters(["bat files (*.bat)"])

        if dlg.exec_():
            files = dlg.selectedFiles()
            if len(files) == 1:
                self.conf_path.setText(files[0])

    def run(self):
        pool_type = str(self.pool_type_list.currentText())
        coin_type = str(self.coin_type_list.currentText())
        conf_path = self.conf_path.text()

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE")
        new_key = winreg.CreateKey(key, "Minerhelper")
        winreg.SetValue(new_key, "pool_type", winreg.REG_SZ, pool_type)
        winreg.SetValue(new_key, "coin_type", winreg.REG_SZ, coin_type)
        winreg.SetValue(new_key, "conf_path", winreg.REG_SZ, conf_path)

        os.chdir(os.path.dirname(conf_path))
        try:
            worker_id = make_id_from_file(conf_path, pool_type, coin_type)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("提示")
            msg.setText("配置信息不正确，请检查文件位置和内容！")
            msg.exec_()
            return

        self.heart_beat_thread = HeartBeatThread(worker_id, conf_path, coin_type)
        self.heart_beat_thread.daemon = True
        self.heart_beat_thread.start()
        self.pool_type_list.setEnabled(False)
        self.coin_type_list.setEnabled(False)
        self.conf_btn.setEnabled(False)
        self.run_btn.setEnabled(False)
        self.auto_run_check.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        # stop the heart beat thread
        self.heart_beat_thread.stop()
        # self.heart_beat_thread.join()

        self.pool_type_list.setEnabled(True)
        self.coin_type_list.setEnabled(True)
        self.conf_btn.setEnabled(True)
        self.run_btn.setEnabled(True)
        self.auto_run_check.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def auto_run_change(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_ALL_ACCESS)
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        app_path = os.path.join(application_path, "矿机助手V2.0.exe")
        app_path = '"' + app_path + '"'
        app_path = app_path.replace('/', '\\')
        bat_path = '"' + self.conf_path.text() + '"'
        bat_path = bat_path.replace('/', '\\')

        # add conf_path to Path environment to enable auto run
        bat_dir = os.path.dirname(self.conf_path.text())
        bat_dir = bat_dir
        bat_dir = bat_dir.replace('/', '\\')
        prepend_env('Path', [bat_dir])

        if self.auto_run_check.isChecked():
            try:
                winreg.SetValueEx(key, "miner_helper", 0, winreg.REG_SZ, app_path + ' "' + application_path + '"')
                winreg.SetValueEx(key, "miner_software", 0, winreg.REG_SZ, bat_path)
            except:
                print(sys.exc_info())
        else:
            try:
                winreg.DeleteValue(key, "miner_helper")
                winreg.DeleteValue(key, "miner_software")

            except EnvironmentError:
                pass

    def closeEvent(self, event):
        try:
            event.accept()
            if self.heart_beat_thread is not None:
                self.stop()
        except Exception as e:
            print(str(e))


def run_miner_software(conf_path):
    os.system('"' + conf_path + '"')


def init():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Minerhelper")
    conf_path = winreg.QueryValue(key, "conf_path")
    # print(conf_path)
    pool_type = winreg.QueryValue(key, "pool_type")
    coin_type = winreg.QueryValue(key, "coin_type")
    return [conf_path, pool_type, coin_type]

if __name__ == "__main__":
    [conf, pool, coin] = [None, None, None]
    try:
        [conf, pool, coin] = init()
    except FileNotFoundError:
        pass
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp(conf, pool, coin)
    window.show()
    sys.exit(app.exec_())
