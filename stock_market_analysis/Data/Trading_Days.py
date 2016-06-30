import datetime


# misc functions for trading days
class TradingDay:
    
    @staticmethod
    def get_today():
        if datetime.datetime.now().hour >= 18:
            return datetime.date.today()
        else:
            return TradingDay.get_yesterday()
    
    @staticmethod
    def get_last_trading_day(date):
        new_date = TradingDay.get_yesterday(date)
        while new_date.weekday() > 4:
            new_date = TradingDay.get_yesterday(new_date)
        return new_date

    @staticmethod
    def get_yesterday(date=None):
        if date is None:
            today = datetime.datetime.today()
        else:
            today = date
        if today.day == 1:
            if today.month == 1:
                yesterday = datetime.date(today.year - 1, 12, 31)
            elif today.month == 2 or today.month == 4 or today.month == 6 or today.month == 8 or today.month == 9 or today.month == 11:
                yesterday = datetime.date(today.year, today.month - 1, 31)
            elif today.month == 3:
                if TradingDay.is_leap_year(today.year):
                    yesterday = datetime.date(today.year, 2, 29)
                else:
                    yesterday = datetime.date(today.year, 2, 28)
            else:
                yesterday = datetime.date(today.year, today.month - 1, 30)
        else:
            yesterday = datetime.date(today.year, today.month, today.day - 1)
        return yesterday

    @staticmethod
    def is_leap_year(year):
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            return True
