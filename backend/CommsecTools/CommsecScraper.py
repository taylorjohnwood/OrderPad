import requests
from . import CommsecScraperConfig 
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib3.exceptions import InsecureRequestWarning
import pandas as pd

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class CommsecScraper(object):
    r""" Web Scrapper for Commsec stock orders.  
    Aquires login cookie by posting to login endpoint.  
    Can retrieve orders from "Manage Orders" page. Includes position in market.
    """

    def __init__(self, loginData=None):
        # Session stores the login cookie
        self.session = requests.sessions.Session()
        self.loginData = loginData

    def performLogin(self):
        "POSTS to login endpoint and stores the login cookie. Must be called before any other scraping."
        
        payload = self._createLoginPayload()
        header = CommsecScraperConfig.LOGIN_HEADER
        res = self.session.post(
            CommsecScraperConfig.LOGIN_POST,
            data=payload,
            headers=header,
            verify=False
        )
        
        if(res.status_code != 200):
            raise Exception("Login was not successful! Please check login information")

    def getOrdersPage(self):
        "GET the Manage Order page. Returns the response."
        header = CommsecScraperConfig.STANDARD_HEADER
        res = self.session.get(CommsecScraperConfig.ORDERS_GET,
                               headers=header, verify=False)
                               # Get the table containing the orders
        return res

    def parseOrdersTable(self, ordersPageHtml):
        soup = BeautifulSoup(ordersPageHtml, 'html.parser')
        table = soup.find('table', id=CommsecScraperConfig.MANAGE_ORDERS_TABLE_ID)
        return table

    def parseOrdersToDf(self, ordersTableHtml):
        r"This function parses the orders page html, to return all orders in a list."
        
        ordersDf = pd.DataFrame(columns  = CommsecScraperConfig.HEADER_ROW)
        rows = ordersTableHtml.find_all('tr')

        for index, row in enumerate(rows):
            cols = row.find_all('td')

            # Use this to filter out random rows
            if(len(cols) != 12):
                continue

            # Strip the text of each column and remove the last column
            cols = [ele.text.strip() for ele in cols[:-1]]

            # Check if the order is a buy or not
            isBuy = True if cols[3] == 'Buy' else False

            # Position in market is the last option. The value attribute is link we need.
            posInMarketOption = row.find_all('option')[-1]
            if(posInMarketOption.text == "Position In Market"):
                posInMarketLinkSuffix = posInMarketOption.get('value')
                posInMarketLink = 'https://www2.commsec.com.au' + posInMarketLinkSuffix
                # Extract the position in the market
                pos = self._getPositionInMarketFromLink(posInMarketLink, isBuy)
            else:
                pos = -1

            cols[-1] = (pos)
            cols.pop(1)
            # Create an empty spot that will be populated by the close price data later on
            cols.insert(7,None)
            cols.pop(1)
            ordersDf.loc[index] = cols

        print(ordersDf)
        return ordersDf

    def setLoginData(self, loginData):
        self.loginData = loginData
        request = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'


    def _getPositionInMarketFromLink(self, link, isBuy):
        header = CommsecScraperConfig.STANDARD_HEADER
        res = self.session.get(link, headers=header, verify=False)

        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', id=CommsecScraperConfig.MARKET_POS_TABLE_ID)
        candidates = table.find_all('td', {'style': 'background-color:Red;'})
        pos = candidates[0].text.strip() if isBuy else candidates[-1].text.strip()
        return int(pos)
    
    def _createLoginPayload(self):
        # This payload is data sent to login post request
        if(self.loginData is None):
            raise Exception('Cannot perform login without login data')
        payload = {
            "__EVENTARGUMENT": '',
            "__EVENTTARGET": '',
            "__VIEWSTATE": "j2wZf0cn4GZwgQ153rsOX2sRMVOPBR5IfTDkge/Jsgl6yD78RQREuDhxWGTo7LID8XMr2bdBO+R6OAL0U0CoFk0SY/v4PhUmGVY3begsv5T5K7FEdC085hJidpAySTy5g2TYwPoEaxa1zLV2abAUDmY/Ghexmkq/eW/gJG7MOUP75YwMNrLW5PXaCt0Mc4FEBGH5KVGypnqXqrmTjr2/HwG1UpuN+XeSFI14I+DxYwOywYlNegsW0hwJqTJc0l5an9Prl8CWnSy+IxzSwBfjTlq8FNMUgk/zhQeAEV71mn0=",
            "__VIEWSTATEGENERATOR": "EBE86427",
            "ctl00$cpContent$btnLogin": "Login",
            "ctl00$cpContent$fakepassword": "Password",
            "ctl00$cpContent$hLegacyStartIn": '',
            "ctl00$cpContent$txtLogin": self.loginData['acc_num'],
            "ctl00$cpContent$txtPassword": self.loginData['password']
        }
        return urlencode(payload)


class ManagedOrders(object):

    def __init__(self):
        None
