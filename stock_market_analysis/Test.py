import django
django.setup()
from stock_market_analysis.Data.models import *

from stock_market_analysis.Data.Data_Calculation import DataCalculation

# DataGather.get_historical_data(ticker='WLL')
DataCalculation.calculate_advanced_stats(ticker='WLL')



