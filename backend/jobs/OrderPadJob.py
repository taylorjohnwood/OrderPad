from ..CommsecTools.CommsecScraper import CommsecScraper
from ..utils.ExcelUtils import createExcelFileFromData
from ..types.TaskStatus import TaskStatus
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import date
import json
import os
import logging
import yfinance as yf
import numpy as np

BASE_PATH = os.getenv('ProgramFiles')

if(BASE_PATH == None):
    BASE_PATH = '/home/taylorwood/Projects/order-queue-position'

class OrderPadJob(QThread):
    taskStatusUpdate = pyqtSignal(str, TaskStatus)
    def __init__(self):
        super().__init__()
        self.commsecScraper = CommsecScraper()
        self.failed = False

    def run(self):
        self.doLogin()
        ordersHtmlPage = self.getOrdersPage()
        orders = self.getMarketPositions(ordersHtmlPage)
        orders = self.getStockClosePrices(orders)
        self.generateExcelFile(orders)
        
    def doLogin(self):
        if self.failed: return None
        self.taskStatusUpdate.emit('Logon to Commsec', TaskStatus.DOING)          
        login_data_path = os.path.abspath(BASE_PATH + '/OrderPad/backend/resources/login_data.json')
        try:
            with open(login_data_path) as f:
                login_data = json.load(f)
        except:
            self.taskStatusUpdate.emit('Logon to Commsec', TaskStatus.FAILED)
            logging.error('Unable to find the login_data file! Aborting OrderPad job')
            self.failed = True
            self.quit()
            return

        self.commsecScraper.setLoginData(login_data)

        try:
            self.commsecScraper.performLogin()
        except:
            logging.error('Commsec refused login data. Check that credentials are correct')
            self.failed = True
            self.quit()
            return

        self.taskStatusUpdate.emit('Logon to Commsec', TaskStatus.SUCCESS)
    
    def getOrdersPage(self):
        if self.failed: return None
        logging.debug('Scanning for orders table')
        self.taskStatusUpdate.emit('Scan for Orders Table', TaskStatus.DOING)
        ordersHtmlPage = self.commsecScraper.getOrdersPage().text
        ordersTableHtml = self.commsecScraper.parseOrdersTable(ordersHtmlPage)

        if(ordersTableHtml == None):
            self.taskStatusUpdate.emit('Scan for Orders Table', TaskStatus.FAILED)
            logging.error('Could not scan for the Orders table')
            self.failed = True
            self.quit()
        else:
            logging.debug(ordersTableHtml)
            
        self.taskStatusUpdate.emit('Scan for Orders Table', TaskStatus.SUCCESS)
        return ordersTableHtml

    def getMarketPositions(self, ordersTableHtml):
        if self.failed: return None
        self.taskStatusUpdate.emit('Get Positions in Market', TaskStatus.DOING)
        
        try:
            logging.debug('Going to parse the orders table html for orders')
            orders = self.commsecScraper.parseOrdersToDf(ordersTableHtml)
        except Exception as error:
            self.taskStatusUpdate.emit('Get Positions in Market', TaskStatus.FAILED)
            logging.error('Parsing Orders failed')
            logging.error(error)
            self.failed=True
            self.quit()

        self.taskStatusUpdate.emit('Get Positions in Market', TaskStatus.SUCCESS)
        return orders

    def getStockClosePrices(self, orders):
        stockTickers = map(lambda x: str(x).strip().upper() + '.AX',list(set(orders['Code'])))
        stockTickerQuery = ' '.join(stockTickers)
        try:
            data = yf.download(stockTickerQuery, threads=False, period='7d', interval='1d', actions=False)
            orders['Close Price ($)'] = [data['Close'][ticker.strip() + '.AX'][data['Close'][ticker.strip() + '.AX'].notnull()][-1] for ticker in orders['Code']]
        except Exception as error: 
            print("Failed to get stock prices.")
        finally:
            return orders

    def generateExcelFile(self, orders):
        if self.failed: return None
        self.taskStatusUpdate.emit('Generate Excel File', TaskStatus.DOING)
        try:
            createExcelFileFromData(orders, 'OrderPad')
        except Exception as e:
            self.taskStatusUpdate.emit('Generate Excel File', TaskStatus.FAILED)
            logging.error('Could not create Excel Report')
            logging.error(e)

        self.taskStatusUpdate.emit('Generate Excel File', TaskStatus.SUCCESS)