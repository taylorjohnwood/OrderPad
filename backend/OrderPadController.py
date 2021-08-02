from .jobs.OrderPadJob import OrderPadJob
from .types.TaskStatus import TaskStatus
import os
import logging

# BASE_PATH = os.path.join(os.environ['MYAPP_HOME'], 'data', 'this_file.dat')

class OrderPadController():
    def __init__(self):
        self.app = None
        self.taskStatuses = {
            'Logon to Commsec': TaskStatus.NOT_STARTED,
            'Scan for Orders Table': TaskStatus.NOT_STARTED,
            'Get Positions in Market': TaskStatus.NOT_STARTED,
            'Generate Excel File': TaskStatus.NOT_STARTED
        }
        self.currentJob = None

    def setApp(self, app):
        self.app = app
        logging.debug('The GUI has registered itself as the controllers application')

    def generateOrderPad(self):
        logging.debug('Creating the OrderPad job instance')
        self.currentJob = OrderPadJob()
        logging.debug('Connecting the statusUpdate signal to the controller')
        self.currentJob.taskStatusUpdate.connect(lambda x,y: self.onTaskStatusUpdate(x,y))
        logging.debug('Starting the OrderPad job')
        try:
            self.currentJob.start()
        except Exception as error:
            logging.debug('Unable to start the OrderPad job')
            logging.error(error)
            
        
    def onTaskStatusUpdate(self, taskName, status):
        self.taskStatuses[taskName] = status
        self.app.taskStatusUpdated(taskName, status)

    def getAllTaskStatuses(self):
        return self.taskStatuses

    def getTaskStatus(self, taskName):
        return self.taskStatuses[taskName]