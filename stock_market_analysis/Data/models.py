from django.db import models


class Stock(models.Model):
    ticker = models.CharField(
        max_length=10,
        blank=False,
        unique=True,
    )

    @classmethod
    def create(cls, ticker):
        stock = cls(ticker=ticker)
        return stock


class DayData(models.Model):
    ticker = models.ForeignKey(Stock, related_name='DailyData', unique_for_date='date')
    day = models.IntegerField(blank=False)
    date = models.DateField(blank=False)
    open = models.IntegerField(blank=True)
    close = models.IntegerField(blank=True)
    high = models.IntegerField(blank=True)
    low = models.IntegerField(blank=True)
    volume = models.IntegerField(blank=True)

    @classmethod
    def create(cls, ticker, day, date, open, close, high, low, volume):
        daydata = cls(ticker=ticker, day=day, date=date, open=open, close=close, high=high, low=low, volume=volume)
        return daydata

    def get_next_day(self):
        return self.day + 1

    def get_previous_day(self):
        return self.day - 1

    def update_values(self, data):
        self.open = data['Open']
        self.close = data['Close']
        self.high = data['High']
        self.low = data['Low']
        self.volume = data['Volume']
        self.save()
