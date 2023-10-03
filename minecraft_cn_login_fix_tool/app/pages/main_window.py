import os

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QHeaderView, QAbstractItemView, QFrame, QTableWidgetItem, QMessageBox
from qfluentwidgets import ScrollArea, PushButton, FluentIcon, TableWidget, StateToolTip

from ...utils.ip_data import *

from ping3 import ping

import re

server_data = []


def takePing(elem):
    return elem["ping"]


class UpdateThread(QThread):
    updateButtonSignal = pyqtSignal(bool)
    fillTableSignal = pyqtSignal(list)
    stateTooltipSignal = pyqtSignal(str, str, bool)
    
    def __init__(self, parent: ScrollArea = None) -> None:
        super().__init__(parent)
    
    def run(self) -> None:
        self.stateTooltipSignal.emit("正在测试各个IP延迟中...",
                                     "这需要一些时间, 请耐心等待!", True)
        new_data = []
        for data in server_data:
            response = ping(data.get("ip"), size=1024, timeout=1)
            if not response:
                response = -1
            else:
                response = int(response * 1000)
            data["ping"] = response
            new_data.append(data)
        new_data.sort(key=takePing)
        
        self.stateTooltipSignal.emit(self.tr("TCPing完成！"), "", False)
        self.fillTableSignal.emit(new_data)
        self.updateButtonSignal.emit(True)


class MainPage(ScrollArea):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.installer_list = []
        self.loader_list = []
        
        self.setWindowIcon(QIcon("resources/icon.ico"))
        self.setWindowTitle("MinecraftCNLoginFixTool")
        
        self.vBoxLayout = QVBoxLayout(self)
        
        self.update_button = PushButton("测试延迟", self, FluentIcon.SYNC)
        self.update_button.clicked.connect(self.__on_update_button_clicked)
        self.confirm_button = PushButton("选取并修改Hosts", self, FluentIcon.PENCIL_INK)
        self.confirm_button.clicked.connect(self.__on_confirm_button_clicked)
        self.delete_button = PushButton("清除本软件修改的hosts", self, FluentIcon.DELETE)
        self.delete_button.clicked.connect(self.__on_delete_button_clicked)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(8, 8, 8, 8)
        self.buttonLayout.addWidget(self.update_button)
        self.buttonLayout.addWidget(self.confirm_button)
        self.buttonLayout.addWidget(self.delete_button)
        
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.setContentsMargins(16, 32, 16, 16)
        
        self.tableFrame = TableFrame(self)
        self.vBoxLayout.addWidget(self.tableFrame)
        
        self.resize(1024, 768)
        
        self.__fill_table()
    
    def __on_update_button_clicked(self):
        self.update_button.setEnabled(False)
        update_thread = UpdateThread(self)
        update_thread.updateButtonSignal.connect(self.__update_data_updateButton_signalReceive)
        update_thread.stateTooltipSignal.connect(self.__update_data_stateTooltip_signalReceive)
        update_thread.fillTableSignal.connect(self.__update_data_fillTable_signalReceive)
        update_thread.start()
    
    def __on_confirm_button_clicked(self):
        hosts_list = []
        new_hosts_list = []
        if self.tableFrame.table.currentRow() == -1:
            return
        data = server_data[self.tableFrame.table.currentRow()]
        for domain in DOMAIN:
            hosts_list.append(data.get("ip") + " " + domain + " #MCLFT_\n")
        try:
            with open("C:/Windows/System32/drivers/etc/hosts", "r", encoding="utf8") as hosts_file:
                origin_hosts_lines = hosts_file.readlines()
            
            with open("C:/Windows/System32/drivers/etc/hosts", "w", encoding="utf8") as hosts_file:
                for line in origin_hosts_lines:
                    if re.search('#MCLFT_', line):
                        continue
                    new_hosts_list.append(line)
                hosts_file.write("".join(new_hosts_list + hosts_list))
                os.popen("ipconfig /flushdns")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e.__class__), QMessageBox.Yes)
        QMessageBox.information(self, '警告', '修改Hosts完成！', QMessageBox.Yes)
    
    def __on_delete_button_clicked(self):
        new_hosts_list = []
        try:
            with open("C:/Windows/System32/drivers/etc/hosts", "r", encoding="utf8") as hosts_file:
                origin_hosts_lines = hosts_file.readlines()
            
            with open("C:/Windows/System32/drivers/etc/hosts", "w", encoding="utf8") as hosts_file:
                for line in origin_hosts_lines:
                    if re.search('#MCLFT_', line):
                        continue
                    new_hosts_list.append(line)
                hosts_file.write("".join(new_hosts_list))
                os.popen("ipconfig /flushdns")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e), QMessageBox.Yes)
        QMessageBox.information(self, '警告', '本软件修改的Hosts删除完毕！', QMessageBox.Yes)
        
    def __update_data_updateButton_signalReceive(self, status):
        self.update_button.setEnabled(status)
    
    def __update_data_stateTooltip_signalReceive(self, title, content, status):
        if status:
            self.stateTooltip = StateToolTip(title, content, self.window())
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()
        else:
            self.stateTooltip.setContent(title)
            self.stateTooltip.setState(True)
            self.stateTooltip = None
    
    def __update_data_fillTable_signalReceive(self, data):
        self.__fill_table(data)
    
    def __fill_table(self, data=None):
        global server_data
        if not data:
            processed_data = []
            for key in IP.keys():
                IP_LIST = IP.get(key)
                for ip in IP_LIST:
                    processed_data.append({"ip": ip, "country": key, "ping": None})
            self.tableFrame.table.setRowCount(len(processed_data))
            for i, data in enumerate(processed_data):
                ip_item = QTableWidgetItem(data.get("ip"))
                ip_item.setTextAlignment(Qt.AlignCenter)
                country_item = QTableWidgetItem(data.get("country"))
                country_item.setTextAlignment(Qt.AlignCenter)
                self.tableFrame.table.setItem(i, 0, ip_item)
                self.tableFrame.table.setItem(i, 1, country_item)
            server_data = processed_data
        else:
            for i, data_ in enumerate(data):
                ip_item = QTableWidgetItem(data_.get("ip"))
                ip_item.setTextAlignment(Qt.AlignCenter)
                country_item = QTableWidgetItem(data_.get("country"))
                country_item.setTextAlignment(Qt.AlignCenter)
                ping_item = QTableWidgetItem(str(data_.get("ping")) if str(data_.get("ping")) != "-1" else "连接超时")
                ping_item.setTextAlignment(Qt.AlignCenter)
                self.tableFrame.table.setItem(i, 0, ip_item)
                self.tableFrame.table.setItem(i, 1, country_item)
                self.tableFrame.table.setItem(i, 2, ping_item)
            server_data = data


class TableFrame(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 8, 0, 0)
        
        # 表格部分
        self.table = TableWidget(self)
        self.table.verticalHeader().hide()
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.table.setHorizontalHeaderLabels([
            "IP",
            "地区",
            "延迟"
        ])
        
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 100)
        
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.vBoxLayout.addWidget(self.table, Qt.AlignLeft)
