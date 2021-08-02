"""
Created by Taylor J Wood, 2021

Version 2.0
"""
from PyQt5.QtWidgets import QApplication, QLabel
from .pages.StatusPage import StatusPage
import os

# BASE_PATH = os.path.join(os.environ['MYAPP_HOME'], 'data', 'this_file.dat')

class OrderPadGui(QApplication):
    def __init__(self, controller=None):
        super().__init__([])
        self.controller = controller
        controller.setApp(self)
        self.statusPage = StatusPage(self)

    def startApp(self):
        self.exec()
    
    def taskStatusUpdated(self, taskName, status):
        self.statusPage.taskStatusUpdated(taskName, status)