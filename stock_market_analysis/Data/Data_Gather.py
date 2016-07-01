import datetime

from constants import logger, INITIAL_DAY
from Tickers import Tickers
from Data_Mapper import DataMapper
from Data_Fetcher import DataFetcher
from Trading_Days import TradingDay


# class used to fetch and map data for all available tickers
class DataGather:

    @staticmethod
    def get_daily_data():
        logger.info("Beginning to gather daily data.")
        start = datetime.datetime.now()
        tickers = Tickers.get_all_tickers()
        for ticker in tickers:
            logger.info("Gathering data for: {}".format(ticker))
            DataMapper.map_data_from_day(ticker, datetime.date.today(), DataFetcher.get_today_stock_data(ticker))
        end = datetime.datetime.now()
        logger.info("Finished gathering daily data. Total time: {}".format(str(end-start)))

    @staticmethod
    def get_historical_data(start=INITIAL_DAY, ticker=None):
        logger.info("Beginning to gather historical data from {}.".format(start.isoformat()))
        start_time = datetime.datetime.now()
        if ticker is None:
            tickers = Tickers.get_all_tickers()
        else:
            tickers = [ticker.upper()]
        for ticker in tickers:
            logger.info("Gathering data for: {}".format(ticker))
            DataMapper.map_historical_data(ticker, DataFetcher.get_historical_stock_data(ticker, start, TradingDay.get_today()))
        end = datetime.datetime.now()
        logger.info("Finished gathering historical data. Total time: {}".format(str(end - start_time)))

    @staticmethod
    def get_company_information():
        logger.info("Beginning to gather company info.")
        start_time = datetime.datetime.now()
        tickers = Tickers.get_all_tickers()
        for ticker in tickers:
            logger.info("Gathering info for: {}".format(ticker))
            DataMapper.map_company_info(ticker, DataFetcher.get_company_info(ticker))
        end = datetime.datetime.now()
        logger.info("Finished gathering company info. Total time: {}".format(str(end - start_time)))