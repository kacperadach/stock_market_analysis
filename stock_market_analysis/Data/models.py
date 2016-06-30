import logging
from django.db import models

logger = logging.getLogger()


class Stock(models.Model):
    ticker = models.CharField(max_length=10, blank=False, unique=True)
    market_cap = models.CharField(max_length=100, blank=True, null=True)
    average_volume = models.IntegerField(blank=True, null=True)
    eps = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    short_ratio = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    pe = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    peg = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)

    @classmethod
    def create(cls, ticker, average_volume=None):
        stock = cls(ticker=ticker, average_volume=average_volume)
        return stock

    def update_values(self, data):
        try:
            self.market_cap = data['Market_cap']
            self.average_volume = data['Average_volume']
            self.eps = data['EPS']
            self.short_ratio = data['Short_ratio']
            self.pe = data['PE']
            self.peg = data['PEG']
        except KeyError:
            logger.warning("Invalid company info for {}".format(self.ticker))


class DayData(models.Model):
    ticker = models.ForeignKey(Stock, related_name='DailyData', unique_for_date='date')
    day = models.IntegerField(blank=False)
    date = models.DateField(blank=False)
    open = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    close = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    high = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    low = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    @classmethod
    def create(cls, ticker, day, date, open, close, high, low, volume):
        daydata = cls(ticker=ticker, day=day, date=date, open=open, close=close, high=high, low=low, volume=volume)
        return daydata

    def update_values(self, data):
        try:
            self.open = data['Open']
            self.close = data['Close']
            self.high = data['High']
            self.low = data['Low']
            self.volume = data['Volume']
            self.save()
        except TypeError as e:
            logger.warning("Error while updating values for {}, {}".format(self.ticker.ticker, e))
        except KeyError as e:
            logger.warning("Error while updating values for {}, {}".format(self.ticker.ticker, e))


class AdvancedStats(models.Model):
    data = models.OneToOneField(DayData)
    rsi = models.IntegerField(blank=True, null=True)

    @classmethod
    def create(cls, rsi):
        advanced_stats = cls(rsi=rsi)
        return advanced_stats

    #def calculate_rsi(self):
