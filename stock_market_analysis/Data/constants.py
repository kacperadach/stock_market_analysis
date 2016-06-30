import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



INITIAL_DAY = datetime.date(2012, 1, 1)


def get_day_int(date):
    return abs(date-INITIAL_DAY).days
