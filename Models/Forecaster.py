import pandas as pd 
import numpy as np
from .Database import Database 
import sqlite3

class Forecaster():
    """
    A class used to forecast the data 
    ...

    Attributes
    ----------
    database : Database      

    Methods
    -------
    double_exponential_smoothin(actuals, alpha, beta)
        Forecast the next value of the currency according to the double 
        exponential method. 
    """

    def __init__(self, database): 
        """
        Parameters
        ----------
        database : Database
            The database where the data of the previous and actual exchange
            rates are saved. 
        currency : str
            The code of the currency we want to forecast.
        """
        self.database = database 

    def forecast(self, curr):
        # if not self.database.tableExists(curr):
        #     print('Table "{}" does not exist'.format(curr))
        #     return
        try: 
            actuals = self.database.readSqliteTable(curr)
            forecast = self.double_exponential_smoothing(actuals["value"], 0.5, 0.5)
            return forecast
        except sqlite3.OperationalError as error: 
            print(error)
        except: 
            print("Il y a eu une erreur avec le forecast")


    def double_exponential_smoothing(self, actuals, alpha, beta):
        """ Use the double exponential to forecast future exchange rates. 
        Parameters
        ----------
        actuals : dataframe
            The time-series of the values we already have for the currency
        alpha : float
            The first parameter of the double exponential, it is the inerty of
            the variation in the currency
        beta : float 
            The second parameter. 
            
        Returns
        -------
        float
            The best estimation of the future currency value according to the 
            forecasting
        """
        size_series = len(actuals)
        
        forecast = np.full(size_series + 1, np.NaN)
        a = np.full(size_series + 1, np.NaN)
        b = np.full(size_series + 1, np.NaN)
        
        a[0] = actuals[0]
        a[1] = actuals[1]
        b[1] = actuals[1] - actuals[0]
        
        for idx in range(2, size_series):
            forecast[idx] = a[idx - 1] + b[idx - 1]
            a[idx] = alpha * actuals[idx] + (1 - alpha) * (a[idx - 1] + b[idx - 1])
            b[idx] = beta * (a[idx] - a[idx - 1]) + (1 - beta) * b[idx - 1]
            
        return a[-2] + b[-2]

