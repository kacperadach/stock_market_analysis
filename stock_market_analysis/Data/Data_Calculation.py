import datetime

from constants import logger
from models import *


class DataCalculation:

    @staticmethod
    def calculate_advanced_stats(ticker=None):
        if ticker is None:
            all_stocks = Stock.objects.all()
        else:
            all_stocks = [Stock.objects.get(ticker=ticker)]
        for stock in all_stocks:
            daily_data = DayData.objects.filter(ticker=stock).order_by('day')
            for data in daily_data:
                adv = AdvancedStats.objects.get_or_create(data=data)[0]
                adv.calculate()
                adv.save()
