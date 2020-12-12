import requests
from datetime import date, datetime
from bs4 import BeautifulSoup
import time
import pandas as pd
from requests_futures.sessions import FuturesSession

class Scraper(): 

    defaultUrl = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
    lastUpdate = date(1970, 1, 1)
    currentReferenceRates = dict()

    def __init__(self, database):
        self.lastUpdate = date(1970, 1, 1)
        self.session = FuturesSession()
        self.currentReferenceRates = ''
        self.database = database

    def getCurrentReferenceRates(self):
        future = self.session.get(self.defaultUrl)
        res = future.result()
        table = BeautifulSoup(res.content, 'html.parser').find('table', {'class' : 'ecb-forexTable fullWidth'})
        actualCurrencyRates = []
        rows = table.find_all('tr')[1:]
        currentRates = dict()
        for row in rows: 
            currentRates[row.find_all('td')[0].text] = float(row.find_all('td')[2].text)
        return currentRates

    def readWithPanda(self):
        df = pd.read_html(self.defaultUrl)
        return df

    def readWithPandaAndSaveToDb(self):
        df = self.readWithPanda(self.defaultUrl)
        self.database.saveDataframe(df)
    