from Models.Fetcher import CurrencyFetcher
from Models.Database import Database
from Models.Forecaster import Forecaster
from Models.Scraper import Scraper

database = Database("Currencies")
fetcher = CurrencyFetcher()
scraper = Scraper(database)
forecaster = Forecaster(database)

curr = input("What is the currency you want to forecast? ")

# database.saveJSON(fetcher.currencyPeriodYear("USD"), "USD")

forecast = forecaster.forecast(curr)
print("The forecast is {} {}".format(round(forecast,3), curr)) 
print("The actual value is  {} {}".format(
    round(scraper.getCurrentReferenceRates()[curr], 3), curr))

database.close()