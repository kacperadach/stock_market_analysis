import django
import datetime
django.setup()
from stock_market_analysis.Data.models import *

from stock_market_analysis.Data.Data_Calculation import DataCalculation
from stock_market_analysis.Data.Data_Gather import DataGather

#DataGather.get_historical_data(ticker='WLL', start=datetime.date(2003,11,20))
# DataGather.get_daily_data(ticker='WLL', )
# DataCalculation.calculate_advanced_stats(ticker='WLL')
# #d = datetime.date(2003, 11, 24)
# d = datetime.date(2016, 7, 1)
# s = Stock.objects.get(ticker='WLL')
# a = AdvancedStats.objects.get(data=DayData.objects.get(ticker=s, date=d))
# print(a.data.day)
# print(a.data.date)
# for b in vars(a):
#     print(b, getattr(a, b))
# total = 0
#


from Algorithms.Historical_Algorithm_Runner import HistoricalAlgorithmRunner
from stock_market_analysis.Algorithms.models import LimitAlgorithm

l = LimitAlgorithm.objects.create(rsi_low=20, rsi_high=80, stoch_low=20, stoch_high=80, mfi_low=20, mfi_high=80, percent_tolerance=0.05)

start = datetime.date(2011, 1, 1)
end = datetime.date(2013, 1, 1)
h = HistoricalAlgorithmRunner(start, end, l, ['WLL'])
h.run()