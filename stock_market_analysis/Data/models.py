from __future__ import division
from django.db import models
from decimal import Decimal
from constants import logger


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

    def get_most_recent_day_data(self):
        return DayData.objects.get(ticker=self, day=DayData.get_day_int(self.ticker)-1)

    def get_most_recent_advanced_stats(self):
        return AdvancedStats.objects.get(data=self.get_most_recent_day_data())

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
        stock = Stock.objects.get(ticker=ticker)
        max = DayData.objects.filter(ticker=stock).aggregate(models.Max('day'))
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
    gain_or_loss = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    fourteen_day_avg_gain = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    fourteen_day_avg_loss = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    fourteen_day_ema_gain =models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    fourteen_day_ema_loss = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    rsi = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    stoch_rsi = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)

    ten_day_ema = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    twenty_day_ema = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    fifty_day_ema = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    twelve_day_ema = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    twenty_six_day_ema = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)
    macd_signal_line = models.DecimalField(decimal_places=17, max_digits=20, blank=True, null=True)

    on_balance_volume = models.IntegerField(blank=True, null=True)

    fourteen_day_pos_flow = models.DecimalField(decimal_places=8, max_digits=20, blank=True, null=True)
    fourteen_day_neg_flow = models.DecimalField(decimal_places=8, max_digits=20, blank=True, null=True)
    money_flow_index = models.IntegerField(blank=True, null=True)

    @classmethod
    def create(cls, data):
        advanced_stats = cls(data=data)
        return advanced_stats

    def get_previous_day_advanced_stats(self):
        if self.data.day != 0:
            return AdvancedStats.objects.get(data=DayData.objects.get(ticker=self.data.ticker, day=self.data.day-1))

    @staticmethod
    def get_simple_moving_average(data):
        data_sum = 0
        for d in data:
            data_sum += d
        return data_sum / len(data)

    @staticmethod
    def get_exponential_moving_average(close, previous_ema, period):
        multiplier = Decimal(2 / (period + 1))
        return ((close - previous_ema) * multiplier) + previous_ema

    def calculate(self):
        self.calculate_rsi()
        self.calculate_stoch_rsi()
        self.calculate_exponential_moving_averages()
        self.calculate_macd_signal_line()
        self.calculate_obv()
        self.calculate_mfi()

    def calculate_mfi(self):
        self.calculate_money_flow_ratio()
        self._calculate_mfi()

    def get_typical_price(self):
        return (self.data.high + self.data.low + self.data.close) / 3

    def calculate_money_flow_ratio(self):
        if self.data.day > 13:
            pos, neg = 0, 0
            for x in range(self.data.day-13, self.data.day+1):
                adv_stats = AdvancedStats.objects.get(data=DayData.objects.get(ticker=self.data.ticker, day=x))
                prev_day = adv_stats.get_previous_day_advanced_stats()
                if adv_stats.get_typical_price() > prev_day.get_typical_price():
                    pos += (adv_stats.get_typical_price() * adv_stats.data.volume)
                elif adv_stats.get_typical_price() < prev_day.get_typical_price():
                    neg += (adv_stats.get_typical_price() * adv_stats.data.volume)
            self.fourteen_day_pos_flow = pos
            self.fourteen_day_neg_flow = neg
            self.save()

    def _calculate_mfi(self):
        if self.data.day > 13:
            if self.fourteen_day_neg_flow == 0:
                self.money_flow_index = 100
            else:
                self.money_flow_index = (100 - (100 / (1 + self.fourteen_day_pos_flow/self.fourteen_day_neg_flow)))
            self.save()

    def calculate_obv(self):
        if self.data.day > 0:
            prev_day = self.get_previous_day_advanced_stats()
            if self.data.day == 1:
                if self.data.close > prev_day.data.close:
                    obv = self.data.volume
                elif self.data.close < prev_day.data.close:
                    obv = -1 * self.data.volume
                else:
                    obv = 0
            else:
                if self.data.close > prev_day.data.close:
                    obv = prev_day.on_balance_volume + self.data.volume
                elif self.data.close < prev_day.data.close:
                    obv = prev_day.on_balance_volume - self.data.volume
                else:
                    obv = prev_day.on_balance_volume
            self.on_balance_volume = obv
            self.save()

    def get_closing_sma(self, period):
        return AdvancedStats.get_simple_moving_average(self._get_simple_moving_average_data(period))

    def calculate_exponential_moving_averages(self):
        for period in (10, 12, 20, 26, 50):
            self._calculate_ema(period)
        self.save()

    def _calculate_ema(self, period):
        ema = None
        if self.data.day == period-1:
            ema = AdvancedStats.get_simple_moving_average(self._get_simple_moving_average_data(period))
        elif self.data.day > period-1:
            previous_close = self._get_previous_ema(period)
            ema = AdvancedStats.get_exponential_moving_average(self.data.close, previous_close, period)
        self._set_ema(period, ema)

    def _set_ema(self, period, ema):
        if period == 10:
            self.ten_day_ema = ema
        elif period == 12:
            self.twelve_day_ema = ema
        elif period == 20:
            self.twenty_day_ema = ema
        elif period == 26:
            self.twenty_six_day_ema = ema
        elif period == 50:
            self.fifty_day_ema = ema
        self.save()

    def _get_simple_moving_average_data(self, period, macd=False):
        data = []
        for x in range(self.data.day-(period-1), self.data.day+1):
            if macd is True:
                data.append(self.get_previous_day_advanced_stats().get_macd())
            else:
                data.append(DayData.objects.get(ticker=self.data.ticker, day=x).close)
        return data

    def calculate_macd_signal_line(self):
        if self.data.day == 34:
            self.macd_signal_line = AdvancedStats.get_simple_moving_average(self._get_simple_moving_average_data(9, macd=True))
        elif self.data.day > 34:
            previous_ema = self._get_previous_ema(9, True)
            self.macd_signal_line = AdvancedStats.get_exponential_moving_average(self.get_macd(), previous_ema, 9)
        self.save()

    def get_macd(self):
        if self.data.day >= 25:
            return self.twelve_day_ema - self.twenty_six_day_ema

    def _get_previous_ema(self, period, macd=False):
        advanced_stats_obj = self.get_previous_day_advanced_stats()
        if macd is True:
            return advanced_stats_obj.macd_signal_line
        elif period == 10:
            return advanced_stats_obj.ten_day_ema
        elif period == 12:
            return advanced_stats_obj.twelve_day_ema
        elif period == 20:
            return advanced_stats_obj.twenty_day_ema
        elif period == 26:
            return advanced_stats_obj.twenty_six_day_ema
        elif period == 50:
            return advanced_stats_obj.fifty_day_ema

    def calculate_rsi(self):
        self.calculate_gain_or_loss()
        self.calculate_fourteen_ema_gain_and_loss()
        self._calculate_rsi(ema=True)

    def calculate_gain_or_loss(self):
        if self.data.day > 0:
            day_before = DayData.objects.get(ticker=self.data.ticker, day=self.data.day-1)
            self.gain_or_loss = ((self.data.close - day_before.close)/day_before.close) * 100
            self.save()

    def calculate_fourteen_ema_gain_and_loss(self):
        if self.data.day == 14:
            gain, loss = 0, 0
            for x in range(1, 15):
                data = AdvancedStats.objects.get(data=DayData.objects.get(ticker=self.data.ticker, day=x))
                if data.gain_or_loss >= 0:
                    gain += data.gain_or_loss
                else:
                    loss += data.gain_or_loss
            self.fourteen_day_ema_gain = gain / 14
            self.fourteen_day_ema_loss = loss / 14
        elif self.data.day > 14:
            prev = self.get_previous_day_advanced_stats()
            if self.gain_or_loss >= 0:
                self.fourteen_day_ema_gain = AdvancedStats.get_exponential_moving_average(self.gain_or_loss, prev.fourteen_day_ema_gain, 14)
                self.fourteen_day_ema_loss = AdvancedStats.get_exponential_moving_average(0, prev.fourteen_day_ema_loss, 14)
            else:
                self.fourteen_day_ema_gain = AdvancedStats.get_exponential_moving_average(0, prev.fourteen_day_ema_gain, 14)
                self.fourteen_day_ema_loss = AdvancedStats.get_exponential_moving_average(abs(self.gain_or_loss), prev.fourteen_day_ema_loss, 14)
        self.save()

    def calculate_fourteen_avg_gain_and_loss(self):
        if self.data.day == 14:
            gain, loss = 0, 0
            for x in range(1, 15):
                data = AdvancedStats.objects.get(data=DayData.objects.get(ticker=self.data.ticker, day=x))
                if data.gain_or_loss >= 0:
                    gain += data.gain_or_loss
                else:
                    loss += data.gain_or_loss
            self.fourteen_day_avg_gain = gain / 14
            self.fourteen_day_avg_loss = abs(loss / 14)
        elif self.data.day > 14:
            data = AdvancedStats.objects.get(data=DayData.objects.filter(ticker=self.data.ticker, day=self.data.day-1))
            if self.gain_or_loss >= 0:
                self.fourteen_day_avg_gain = (((data.fourteen_day_avg_gain * 13) + self.gain_or_loss) / 14)
                self.fourteen_day_avg_loss = abs(((data.fourteen_day_avg_loss * 13) / 14))
            else:
                self.fourteen_day_avg_loss = abs((((data.fourteen_day_avg_loss * 13) + self.gain_or_loss) / 14))
                self.fourteen_day_avg_gain = ((data.fourteen_day_avg_gain * 13) / 14)
        self.save()

    def _calculate_rsi(self, ema=False):
        if self.data.day > 13:
            if ema:
                rs = self.fourteen_day_ema_gain / self.fourteen_day_ema_loss
            else:
                rs = self.fourteen_day_avg_gain / self.fourteen_day_avg_loss
            if self.fourteen_day_avg_loss == 0:
                self.rsi = 100
            else:
                self.rsi = 100 - (100 / (1 + rs))
            self.save()

    def _find_fourteen_day_high_low_rsi(self):
        low, high = None, None
        for x in range(self.data.day-13, self.data.day+1):
            data = AdvancedStats.objects.get(data=DayData.objects.filter(ticker=self.data.ticker, day=x))
            if low is None or low > data.rsi:
                low = data.rsi
            elif high is None or high < data.rsi:
                high = data.rsi
        return {'high': high, 'low': low}

    def calculate_stoch_rsi(self):
        if self.data.day >= 26:
            high_low = self._find_fourteen_day_high_low_rsi()
            high, low = high_low['high'], high_low['low']
            self.stoch_rsi = ((self.rsi - low) / (high - low)) * 100
            self.save()
