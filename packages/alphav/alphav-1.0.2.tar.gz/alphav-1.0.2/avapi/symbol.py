import time

import requests
from .data import PullDataDescriptor

rejected = {'Note':
                'Thank you for using Alpha Vantage! Our standard API call frequency '
                'is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ '
                'if you would like to target a higher API call frequency.'}


class Symbol:
    # company data
    balance_sheet = PullDataDescriptor()
    earnings = PullDataDescriptor()
    income_statement = PullDataDescriptor()
    cash_flow = PullDataDescriptor()

    # stock data
    overview = PullDataDescriptor()
    global_quote = PullDataDescriptor()

    # detailed stock data
    time_series_daily = PullDataDescriptor()
    time_series_monthly = PullDataDescriptor()
    time_series_monthly_adjusted = PullDataDescriptor()
    time_series_weekly = PullDataDescriptor()
    time_series_weekly_adjusted = PullDataDescriptor()

    def __init__(self, symbol: str, key, sleep=60):
        """
        main object to receive stock data for, using ticker / symbol as key
        :param symbol: unique stock ticker
        :param key: alpha vantage api key
        :param sleep: sleep time when getting rejected from server
        """
        self._key = key
        self._symbol = symbol
        self._sleep = sleep

    @property
    def sleep(self):
        """
        :return: sleep time when getting rejected from server
        """
        return self._sleep

    @property
    def symbol(self):
        """
        :return: symbol / ticker for this quote
        """
        return self._symbol

    @property
    def key(self):
        """
        :return: alpha vantage api key
        """
        return self._key

    def req(self, function: str):
        """
        request data from api
        :param function: api function
        :return: raw data
        """
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self._symbol}&apikey={self.key}'
        r = requests.get(url)
        data = r.json()
        if data == rejected:
            print(f'got rejected, sleeping for: {self.sleep}..')
            time.sleep(self.sleep)
            data = self.req(function)
        return data
