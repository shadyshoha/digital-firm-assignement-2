import requests
from datetime import datetime, date
import json


class CurrencyFetcher():

    defaultHost = 'api.frankfurter.app'

    def __init__(self, host=defaultHost):
        self.host = host

    def getOneCurrencyValue(self, curr, date=datetime.now()):
        res = requests.get(
            'https://{}/latest?amount=10&from=GBP&to=USD'.format(self.host))
        return res

    def getCurrencies(self):
        currencies = requests.get(
            'https://{host}/currencies'.format(host=self.host)).json()  # https://api.frankfurter.app/currencies
        return currencies

    def getCurrencies(self):
        url = "https://api.frankfurter.app/currencies"
        # transform the text in dictionnary
        currencies = requests.get(url).json()
        print(currencies["USD"])
        # United States Dollar

    def getCurrencyName(self, currencyCode):
        currencies = self.getCurrencies()
        return currencies[currencyCode]

    def getATimeSerie(self, currencyCode, beginPeriod, endPeriod=date.today()):
        params = {'to': currencyCode}
        url = 'https://{host}/{beginDate}..'.format(
            host=self.host, beginDate=beginPeriod.strftime('%Y-%m-%d'))  # Transformer la date en string
        # Format de l'url
        # Documentation différents moyen de récupérer
        # Une requête par jour paér Currency
        # Une requête pour tout
        text_rates = requests.get(url, params=params)
        rates = text_rates.json()
        # Transformation
        return rates  # dictionnaire

    def currencyPeriodYear(self, currencyCode, date=datetime.today()):
        return self.getATimeSerie(currencyCode, datetime(year=date.year-1, month=date.month, day=date.day))
