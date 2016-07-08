from stock_market_analysis.Data.models import Stock, DayData
from stock_market_analysis.Misc.Time_Logger import time_logger
from constants import logger


class HistoricalAlgorithmRunner:

    def __init__(self, start_date, end_date, algorithm, stocks=None):
        self.start_date = start_date
        self.end_date = end_date
        self.algorithm = algorithm
        self.stocks = stocks

    @time_logger("running algorithm on historical data")
    def run(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            self.algorithm.update_transaction_data(current_date)
            if self.stocks is None:
                data = DayData.objects.filter(date=current_date)
            else:
                data = []
                for ticker in self.stocks:
                    s = Stock.objects.get(ticker=ticker.upper())
                    data.append(DayData.objects.filter(ticker=s, date=current_date))
            for d in data:
                self.algorithm.run(d)
        self.algorithm.delete_all_incomplete_transactions()
        self.log_finished_algorithm_test()

    def log_finished_algorithm_test(self):
        logger.info("Ran algorithm {} from {} to {}".format(self.algorithm.name, self.start_date, self.end_date))
        logger.info("Total Return: {}".format(self.algorithm.get_overall_return()))
