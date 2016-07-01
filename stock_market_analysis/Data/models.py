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
    day = models.IntegerField(blank=False, unique=True)
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

    @staticmethod
    def get_day_int(ticker):
        stock = Stock.objects.filter(ticker=ticker)
        max = DayData.objects.all().aggregate(models.Max('day'))
        if max['day__max'] is None:
            return 0
        else:
            return max['day__max'] + 1

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
    data = models.OneToOneField(DayData, blank=True, null=True, related_name='Advanced_Stats')
    gain_or_loss = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    fourteen_day_avg_gain = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    fourteen_day_avg_loss = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    rsi = models.IntegerField(blank=True, null=True)

    @classmethod
    def create(cls, data):
        advanced_stats = cls(data=data)
        return advanced_stats

    def calculate(self):
        self.calculate_rsi()

    def calculate_rsi(self):
        self.calculate_gain_or_loss()
        self.calculate_fourteen_avg_gain_and_loss()
        self._calculate_rsi()

    def calculate_gain_or_loss(self):
        if self.data.day == 0:
            self.gain_or_loss = ((self.data.close - self.data.open)/self.data.open) * 100
        else:
            day_before = DayData.objects.get(ticker=self.data.ticker, day=self.data.day-1)
            self.gain_or_loss = ((self.data.close - day_before.close)/day_before.close) * 100
        self.save()

    def calculate_fourteen_avg_gain_and_loss(self):
        if self.data.day == 13:
            gain, loss = 0, 0
            for x in range(self.data.day-13, self.data.day+1):
                data = AdvancedStats.objects.get(data=DayData.objects.filter(ticker=self.data.ticker, day=x))
                if data.gain_or_loss >= 0:
                    gain += data.gain_or_loss
                else:
                    loss += data.gain_or_loss
            self.fourteen_day_avg_gain = gain / 14
            self.fourteen_day_avg_loss = loss / 14
        elif self.data.day > 13:
            data = AdvancedStats.objects.get(data=DayData.objects.filter(ticker=self.data.ticker, day=self.data.day-1))
            if self.gain_or_loss >= 0:
                self.fourteen_day_avg_gain = (((data.fourteen_day_avg_gain * 13) + self.gain_or_loss) / 14)
                self.fourteen_day_avg_loss = ((data.fourteen_day_avg_loss * 13) / 14)
            else:
                self.fourteen_day_avg_loss = (((data.fourteen_day_avg_loss * 13) + self.gain_or_loss) / 14)
                self.fourteen_day_avg_gain = ((data.fourteen_day_avg_gain * 13) / 14)
        self.save()

    def _calculate_rsi(self):
        if self.data.day > 12:
            if self.fourteen_day_avg_loss == 0:
                self.rsi = 100
            else:
                self.rsi = 100 - (100 / (1 + abs((self.fourteen_day_avg_gain/self.fourteen_day_avg_loss))))
            self.save()
