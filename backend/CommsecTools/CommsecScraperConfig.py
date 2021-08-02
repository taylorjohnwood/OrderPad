LOGIN_POST = 'https://www2.commsec.com.au/Public/HomePage/Login.aspx'
ORDERS_GET = 'https://www2.commsec.com.au/Private/EquityTrading/AustralianShares/ManageOrders.aspx'
MANAGE_ORDERS_TABLE_ID = 'ctl00_BodyPlaceHolder_OrderStatusView1_OrderOutstanding_gvOrdersOutstanding_Underlying'
MARKET_POS_TABLE_ID = 'ctl00_BodyPlaceHolder_PositionInMarketView1_ucPositionInMarket_grdPositionInMarket_Underlying'

STANDARD_HEADER = {
            "sec-ch-ua": "\"Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Upgrade-Insecure-Requests": '1',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

LOGIN_HEADER = STANDARD_HEADER.copy()
LOGIN_HEADER.update({"Content-Type": "application/x-www-form-urlencoded"})
API_KEY = "XGXIEJDFGRBT5IR2"
HEADER_ROW = [
    "Order Date",
    # "Order Number",	
    "Type",
    "Code",	
    "Quantity Ordered",	
    "Quantity Outstanding",
    "Quantity Executed",
    'Close Price ($)',
    "Order Price ($)",
    "Expiry Date",
    "Position"
]