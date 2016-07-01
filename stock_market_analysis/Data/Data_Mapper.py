import datetime

from models import *


# class used to Map data to model objects
class DataMapper:

    @staticmethod
    def map_historical_data(ticker, data):
        try:
            for d in data:
                if DataMapper._is_valid_data(d):
                    DataMapper.map_data_from_day(ticker, d['Date'], d)
        except TypeError:
            logger.warning("Invalid data given for {} while mapping historical data".format(ticker))

    @staticmethod
    def map_data_from_day(ticker, date, data):
        s = Stock.objects.get_or_create(ticker=ticker)[0]
        dd = DayData.objects.get_or_create(ticker=s, day=(DayData.get_day_int(ticker)), date=date)[0]
        dd.update_values(data)
        s.save()

    @staticmethod
    def map_company_info(ticker, data):
        s = Stock.objects.get_or_create(ticker=ticker)[0]
        s.update_values(data)
        s.save()

    @staticmethod
    def _is_valid_data(data):
        for key in ('Open', 'Close', 'High', 'Low', 'Volume', 'Date'):
            if key not in data:
                return False
        return True
