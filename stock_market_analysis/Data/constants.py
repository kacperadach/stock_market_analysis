import datetime

INITIAL_DAY = datetime.date(2012, 1, 1)


def get_day_int(date):
    return abs(date-INITIAL_DAY).days
