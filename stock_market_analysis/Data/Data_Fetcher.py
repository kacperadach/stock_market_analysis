import datetime

from yahoo_finance import Share, YQLQueryError

from constants import logger


# class used to fetch daily and historical data for a given ticker
class DataFetcher(object):

    @staticmethod
    def get_today_stock_data(ticker):
        try:
            s = Share(ticker)
            data = {
                'Open': float(s.get_open()),
                'Close': float(s.get_prev_close()),
                'High': float(s.get_days_high()),
                'Low': float(s.get_days_low()),
                'Volume': int(s.get_volume()),
                'Date': datetime.date.today(),
            }
            return data
        except YQLQueryError:
            logger.error("Daily data not found for {}".format(ticker))
        except Exception as e:
            logger.error("Unexpected error occured: {}".format(e))
        return {}

    @staticmethod
    def get_historical_stock_data(ticker, start_date, end_date):
        try:
            s = Share(ticker)
            start_date, end_date = start_date.isoformat(), end_date.isoformat()
            data = s.get_historical(start_date, end_date)
            arr = []
            for day in data:
                arr.append(DataFetcher._extract_data(day))
            return arr
        except YQLQueryError:
            logger.error("Historical data not found for {}".format(ticker))
        return []

    @staticmethod
    def get_company_info(ticker):
        try:
            s = Share(ticker)
            data = {
                'Market_cap': s.get_market_cap(),
                'Average_volume': s.get_avg_daily_volume(),
                'EPS': s.get_earnings_share(),
                'Short_ratio': s.get_short_ratio(),
                'PE': s.get_price_earnings_ratio(),
                'PEG': s.get_price_earnings_growth_ratio(),
            }
            return DataFetcher._extract_company_info(data)
        except YQLQueryError:
            logger.error("Company info not found for {}".format(ticker))
        except Exception as e:
            logger.error("Unexpected error occured: {}".format(e))
        return {}

    @staticmethod
    def get_extra_field(ticker, date, field):
        try:
            s = Share(ticker)
            date = date.isoformat()
            data = s.get_historical(date, date)[0]
            try:
                value = data[field]
                return value
            except KeyError as e:
                logger.error('KeyError: {}, while trying to access {} field'.format(e, field))
        except YQLQueryError:
            logger.error("Error gathering data for {}".format(ticker))
        return None

    @staticmethod
    def _extract_data(data):
        for key, val in data.items():
            if key == 'Volume':
                data[key] = int(val)
            elif key == 'Date':
                date = datetime.datetime.strptime(val, '%Y-%m-%d')
                data[key] = datetime.date(date.year, date.month, date.day)
            elif key in ('Open', 'Close', 'High', 'Low', 'Volume', 'Date'):
                data[key] = float(val)
        return data

    @staticmethod
    def _convert_market_cap(cap):
        if cap is None:
            return None
        elif cap.endswith('B'):
            return float(cap[:-1]) * 1000000000
        elif cap.endswith('M'):
            return float(cap[:-1]) * 1000000
        else:
            logger.warning("Market cap does not end with B or M, {}".format(cap))
            return None

    @staticmethod
    def _extract_company_info(data):
        for key, val in data.items():
            try:
                if key == 'Market_cap':
                    data[key] = DataFetcher._convert_market_cap(val)
                elif key == 'Average_volume':
                    data[key] = int(val)
                else:
                    data[key] = float(val)
            except:
                pass
        return data