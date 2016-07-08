import datetime

from functools import wraps

from stock_market_analysis.Data.constants import logger


def time_logger(text):
    def time_logger_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            logger.info("Starting task: {}".format(text))
            start = datetime.datetime.now()
            func(*args, **kwargs)
            end = datetime.datetime.now()
            logger.info("Finished task: {}. Total time: {}".format(text, str(end-start)))
        return func_wrapper
    return time_logger_decorator



