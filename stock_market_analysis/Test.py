import django
django.setup()

from stock_market_analysis.Data.Data_Gather import DataGather

DataGather.get_historical_data()