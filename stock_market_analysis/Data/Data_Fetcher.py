import logging
from yahoo_finance import Share

logger = logging.getLogger()


# class used to fetch data for a given ticker
class DataFetcher(object):

    @staticmethod
    def get_stock_data(ticker, date):
        s = Share(ticker)
        date = date.isoformat()
        try:
            data = s.get_historical(date, date)[0]
        except IndexError:
            logger.error('Invalid API call: No data found for {} on {}'.format(ticker, date))
        else:
            return DataFetcher.extract_data(data)



    @staticmethod
    def get_extra_field(ticker, date, field):
        s = Share(ticker)
        date = date.isoformat()
        try:
            data = s.get_historical(date, date)[0]
        except IndexError as e:
            logger.error('Invalid API call: No data found for {} on {}'.format(ticker, date))
        else:
            try:
                value = data[field]
                return value
            except KeyError as e:
                logger.error('KeyError: {}, while trying to access {} field'.format(e, field))
                return None

    @staticmethod
    def extract_data(data):
        arr = {'Open': data['Open'], 'Close': data['Close'], 'High': data['High'], 'Low': data['Low'], 'Volume': data['Volume']}
        return arr

    @staticmethod
    def get_historical_stock_data(ticker, start_date, end_date):
        s = Share(ticker)
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        data = s.get_historical(start_date, end_date)
        arr = []
        for day in data:
            arr.append(DataFetcher.extract_data(day))
        return arr




