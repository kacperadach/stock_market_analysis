import datetime

from constants import logger, INITIAL_DAY
from Tickers import Tickers
from Data_Mapper import DataMapper
from Data_Fetcher import DataFetcher
from Trading_Days import TradingDay

from stock_market_analysis.Misc.Time_Logger import time_logger


# class used to fetch and map data for all available tickers
class DataGather:

    @staticmethod
    @time_logger("gathering daily data")
    def get_daily_data(ticker=None):
        if ticker is None:
            tickers = Tickers.get_all_tickers()
        else:
            tickers = [ticker]
        for ticker in tickers:
            logger.info("Gathering data for: {}".format(ticker))
            DataMapper.map_data_from_day(ticker, datetime.date.today(), DataFetcher.get_today_stock_data(ticker))


    @staticmethod
    @time_logger("gathering historical data")
    def get_historical_data(start=INITIAL_DAY, ticker=None):
        if ticker is None:
            tickers = Tickers.get_all_tickers()
        else:
            tickers = [ticker.upper()]
        for ticker in tickers:
            logger.info("Gathering data for: {}".format(ticker))
            DataMapper.map_historical_data(ticker, DataFetcher.get_historical_stock_data(ticker, start, TradingDay.get_today()))

    @staticmethod
    @time_logger("gathering company info")
    def get_company_information():
        tickers = Tickers.get_all_tickers()
        for ticker in tickers:
            logger.info("Gathering info for: {}".format(ticker))
            DataMapper.map_company_info(ticker, DataFetcher.get_company_info(ticker))
