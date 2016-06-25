from stock_market_analysis.Data.API_URL_builder import URLBuilder
from stock_market_analysis.Data.SpecialTagEnum import SpecialTag
from stock_market_analysis.Data.API_Data_Fetcher import DataFetcher
from datetime import date


str = URLBuilder.get_daily_url('trup', SpecialTag.previous_close, SpecialTag.open)
print(str)

str = URLBuilder.get_range_url('trup', date(2016, 6, 1), date(2016, 6, 7))
print(str)

print(DataFetcher.fetch(str))
