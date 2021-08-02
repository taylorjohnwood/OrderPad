from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from .WaitingSpinner import QtWaitingSpinner
from enum import IntEnum
import os

BASE_PATH = os.getenv('ProgramFiles')

if(BASE_PATH == None):
    BASE_PATH = '/home/taylorwood/Projects/order-queue-position'
class TaskStatus(IntEnum):
    NOT_STARTED = 0
    DOING = 1
    FAILED = 2
    SUCCESS = 3

class StatusDisplay(QFrame):
    def __init__(self, label="", status=TaskStatus.NOT_STARTED):
        super().__init__()
        self.label = QLabel(label)
        self.status = status
        self.spinner = self._buildSpinner()
        self.success_icon = QIcon(BASE_PATH + '/OrderPad/gui/resources/tick.png').pixmap(QSize(64,64))
        self.failed_icon = QIcon(BASE_PATH + '/OrderPad/gui/resources/cross.png').pixmap(QSize(64,64))
        self.icon = QLabel()
        self.layout = QHBoxLayout(self)
        self._initWidgets()
        self.hide()

    def setStatus(self, status):
        self.status = TaskStatus(status)
        self.refreshStatusIcon()
    
    def refreshStatusIcon(self):
        if(self.status == TaskStatus.DOING):
            self.icon.hide()
            self.spinner.start()

        elif(self.status == TaskStatus.FAILED):
            self.spinner.stop()
            self.icon.setPixmap(self.failed_icon)
            self.icon.show()
        elif(self.status == TaskStatus.SUCCESS):
            self.spinner.stop()
            self.icon.setPixmap(self.success_icon)
            self.icon.show()
        else:
            self.icon.hide()
            self.spinner.stop()
           

    def _initWidgets(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinner)
        self.layout.addWidget(self.icon)

    def _buildSpinner(self):
        spinner = QtWaitingSpinner(self, centerOnParent=False)
        spinner.stop()
        spinner.setRevolutionsPerSecond(1)
        return spinner

def buildStatusDisplays(statuses):
        widgets = [StatusDisplay(statusName) for statusName in statuses.keys()]
        return dict(zip(statuses.keys(), widgets))