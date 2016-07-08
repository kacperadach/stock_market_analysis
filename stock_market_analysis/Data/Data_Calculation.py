from models import *
from stock_market_analysis.Misc.Time_Logger import time_logger

class DataCalculation:

    @staticmethod
    @time_logger("calculating advanced stats")
    def calculate_advanced_stats(ticker=None, date=None):
        if ticker is None:
            all_stocks = Stock.objects.all()
        else:
            all_stocks = [Stock.objects.get(ticker=ticker)]
        for stock in all_stocks:
            logger.info("calculating advanced stats for {}".format(stock.ticker))
            if date is None:
                daily_data = DayData.objects.filter(ticker=stock).order_by('day')
            else:
                daily_data = [DayData.objects.get(ticker=stock, date=date)]
            for data in daily_data:
                logger.info("calculating day {}".format(data.day))
                adv = AdvancedStats.objects.get_or_create(data=data)[0]
                adv.calculate()
