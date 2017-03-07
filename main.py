# -*- coding: utf-8 -*-
import sys
import os
# from PyQt4 import QtGui, uic
# from PyQt4.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
import winreg
from hbthread import HeartBeatThread

from util2 import *

qtCreatorFile = "./main.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, conf_path=None, pool_type=None, coin_type=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("矿机助手V2.0")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        pool_list = [F2POOL, ETHFANS]
        coin_list = [ETH, ZEC]
        self.pool_type_list.addItems(pool_list)
        self.coin_type_list.addItems(coin_list)
        self.conf_btn.clicked.connect(self.select_file_path)
        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)
        self.heart_beat_thread = None

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
        self.stop_btn.setEnabled(True)

    def stop(self):
        # stop the heart beat thread
        self.heart_beat_thread.stop()
        # self.heart_beat_thread.join()

        self.pool_type_list.setEnabled(True)
        self.coin_type_list.setEnabled(True)
        self.conf_btn.setEnabled(True)
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)


def init():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Minerhelper")
        conf_path = winreg.QueryValue(key, "conf_path")
        print(conf_path)
        pool_type = winreg.QueryValue(key, "pool_type")
        coin_type = winreg.QueryValue(key, "coin_type")
        return [conf_path, pool_type, coin_type]
        # [address, worker] = get_address_worker(conf_path)
        # worker_id = make_id(pool_type, coin_type, address, worker)
        # print(worker_id)
        # os.chdir(os.path.dirname(conf_path))
        # heart_beat_thread = HeartBeatThread(worker_id, conf_path, coin_type)
        # heart_beat_thread.daemon = True
        # heart_beat_thread.start()
        # heart_beat_thread.join()
        # heart_beat(id)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    [conf_path, pool_type, coin_type] = init()
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp(conf_path, pool_type, coin_type)
    window.show()
    sys.exit(app.exec_())
