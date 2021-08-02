from gui.OrderPadGui import OrderPadGui
from backend.OrderPadController import OrderPadController
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

# if __name__=='__main__.py':
app = OrderPadGui(OrderPadController())
app.startApp()