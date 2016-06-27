import datetime

from stock_market_analysis.Data.constants import get_day_int
from stock_market_analysis.Data.Data_Fetcher import DataFetcher
from stock_market_analysis.Data.models import *


# class used to Map data to model objects
class DataMapper:

    @staticmethod
    def get_data_from_day(ticker, date):
        return DataFetcher.get_stock_data(ticker, date)

    @staticmethod
    def map_data_from_day(ticker, date, data):
        s = Stock.objects.get_or_create(ticker=ticker)[0]
        dd = DayData.objects.get_or_create(ticker=s, day=(get_day_int(date)), date=date)[0]
        dd.update_values(data)
        s.save()

    @staticmethod
    def map_data_from_today(ticker):
        today = DataMapper.get_today()
        DataMapper.map_data_from_day(ticker, today, DataMapper.get_data_from_day(ticker, today))

    @staticmethod
    def map_historical_data(ticker, start, end=None):
        if end is None:
            end = datetime.datetime.today()
        data = DataFetcher.get_historical_stock_data(ticker, start, end)
        current = end
        for d in data:
            DataMapper.map_data_from_day(ticker, current, d)
            current = DataMapper.get_yesterday(current)

    @staticmethod
    def get_today():
        time = datetime.datetime.now().time()
        if time.hour > 16:
            return datetime.date.today()
        else:
            return DataMapper.get_yesterday()

    @staticmethod
    def get_yesterday(date=None):
        if date == None:
            today = datetime.datetime.today()
        if today.day == 1:
            if today.month == 1:
                yesterday = datetime.date(today.year -1, 12, 31)
            elif today.month == 2 or today.month == 4 or today.month == 6 or today.month == 8 or today.month == 9 or today.month == 11:
                yesterday = datetime.date(today.year, today.month - 1, 31)
            elif today.month == 3:
                if DataMapper._is_leap_year():
                    yesterday = datetime.date(today.year, 2, 29)
                else:
                    yesterday = datetime.date(today.year, 2, 28)
            else:
                yesterday = datetime.date(today.year, today.month - 1, 30)
        else:
            yesterday = datetime.date(today.year, today.month, today.day - 1)
        return yesterday

    @staticmethod
    def _is_leap_year():
        year = datetime.datetime.today().year
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            return True
