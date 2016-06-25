from django.db import models


class Stock(models.Model):
    ticker = models.CharField(
        max_length=10,
        blank=False,
        unique=True,
    )


class DayData(models.Model):
    ticker = models.ForeignKey(Stock, related_name='DailyData', unique_for_date='date')
    day = models.IntegerField(blank=False)
    date = models.DateField(blank=False)


class StockData(models.Model):
    for_day = models.ForeignKey(DayData, related_name='Data')
    open = models.IntegerField(blank=False)
    close = models.IntegerField(blank=False)
    high = models.IntegerField(blank=False)
    low = models.IntegerField(blank=False)

    def __init__(self, open, close, high, low):
        super(StockData, self).__init__()
        self.open = open
        self.close = close
        self.high = high
        self.low = low

    @classmethod
    def create(cls, open, close, high, low):
        return cls(open, close, high, low)
