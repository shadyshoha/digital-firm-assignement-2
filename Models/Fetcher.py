import requests
from datetime import datetime, date
import json 

class CurrencyFetcher():

    defaultHost = 'api.frankfurter.app'

    def __init__(self, host=defaultHost):
        self.host = host
        
    def getOneCurrencyValue(self, curr, date=datetime.now()):
        res = requests.get('https://{}/latest?amount=10&from=GBP&to=USD'.format(self.host))
        return res

    def getCurrencies(self):
        currencies = requests.get('https://{host}/currencies'.format(host=self.host)).json()
        return currencies

    def getCurrencyName(self, currencyCode):
        currencies = self.getCurrencies()
        return currencies[currencyCode]

    def getATimeSerie(self, currencyCode, beginPeriod, endPeriod=date.today()):
        params = { 'to' : currencyCode }
        if endPeriod==date.today() :
            url = 'https://{host}/{beginDate}..'.format(host=self.host, beginDate=beginPeriod.strftime('%Y-%m-%d'))
        print(url)
        rates = requests.get(url, params=params).json()
        return rates

    def currencyPeriodYear(self, currencyCode, date=datetime.today()):
        return self.getATimeSerie(currencyCode, datetime(year=date.year-1, month=date.month, day=date.day))


