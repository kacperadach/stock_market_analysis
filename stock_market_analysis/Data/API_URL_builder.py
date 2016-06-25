import logging
from datetime import date
from stock_market_analysis.Data.SpecialTagEnum import SpecialTag

BASEURL = "http://finance.yahoo.com/d/quotes.csv?s="
EXTRATAG = "&f="
BASEURL_RANGE = 'http://ichart.finance.yahoo.com/table.csv?s='
EXTRATAG_RANGE = '&ignore=.csv'


class URLBuilder(object):

    @staticmethod
    def get_daily_url(ticker, *args):
        url = "" + BASEURL + ticker + EXTRATAG
        return URLBuilder._add_tags(url, *args)

    @staticmethod
    def get_range_url(ticker, start_date, end_date):
        today = date.today()
        if start_date > end_date:
            raise ValueError
        elif end_date >= today:
            raise  ValueError
        else:
            url = "" + BASEURL_RANGE + ticker
            url += "&a=" + str(start_date.month - 1) + "&b=" + str(start_date.day) + "&c=" + str(start_date.year)
            url += "&d=" + str(end_date.month - 1) + "&e=" + str(end_date.day) + "&f=" + str(end_date.year)
            url += "&g=d"
            return url + EXTRATAG_RANGE

    @staticmethod
    def _add_tags(url, *args):
        try:
            for a in args:
                url += SpecialTag.get_string(a)
        except AttributeError as e:
            logging.error("Invalid stock data parameter: {}".format(e))
        return url