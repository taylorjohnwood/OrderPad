from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ..components.StatusDisplay import StatusDisplay, buildStatusDisplays, TaskStatus

class StatusPage(QWidget):
    def __init__(self, parent):
        self.parent = parent
        self.controller = self.parent.controller
        self.taskStatuses = self.controller.getAllTaskStatuses()
        self.statusDisplays = None
        self._initGui()
        self.controller.generateOrderPad()
    
    def taskStatusUpdated(self, taskName, status):
        self.statusDisplays[taskName].setStatus(status)
        
    def _initGui(self):
        super().__init__()
        self.setWindowTitle("OrderPad")
        self.layout = QVBoxLayout(self)
        self._initWidgets()
        self.show()

    def _initWidgets(self):
        self.statusDisplays = buildStatusDisplays(self.taskStatuses)
        for widget in self.statusDisplays.values():
            self.layout.addWidget(widget)
            widget.show()

