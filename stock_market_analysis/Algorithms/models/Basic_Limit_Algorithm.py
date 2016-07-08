from django.db import models

from stock_market_analysis.BaseAlgorithmApp.models import Algorithm, Transaction
from stock_market_analysis.Data.models import DayData


class LimitAlgorithm(Algorithm):

    rsi_low = models.IntegerField(blank=False)
    rsi_high = models.IntegerField(blank=False)
    stoch_low = models.IntegerField(blank=False)
    stoch_high = models.IntegerField(blank=False)
    mfi_low = models.IntegerField(blank=False)
    mfi_high = models.IntegerField(blank=False)
    percent_tolerance = models.DecimalField(max_digits=5, decimal_places=5)

    class Meta:
        app_label = 'Algorithms'
        db_table = 'limitalgorithm'

    #
    # @classmethod
    # def create(cls, rsi_low, rsi_high, stoch_low, stoch_high, mfi_low, mfi_high, percent_tolerance):
    #     return cls(name='Basic Limit Algorithm', rsi_low=rsi_low, rsi_high=rsi_high, stoch_low=stoch_low, stoch_high=stoch_high,
    #                mfi_low=mfi_low, mfi_high=mfi_high, percent_tolerance=percent_tolerance)

    def go_long(self, adv_data):
        if self._check_limits_long(adv_data):
            if adv_data.get_macd() > 0 and adv_data.macd_signal_line <= adv_data.get_macd():
                if adv_data.ten_day_ema > adv_data.twenty_day_ema > adv_data.fifty_day_ema:
                    return True
        return False

    def go_short(self, adv_data):
        if self._check_limits_short(adv_data):
            if adv_data.get_macd() < 0 and adv_data.macd_signal_line >= adv_data.get_macd():
                if adv_data.ten_day_ema < adv_data.twenty_day_ema and adv_data.ten_day_ema < adv_data.fifty_day_ema:
                    return True
        return False

    def _check_limits_long(self, adv_data):
        return adv_data.rsi < self.rsi_low and adv_data.stoch_rsi < self.stoch_low and adv_data.money_flow_index < self.mfi_low

    def _check_limits_short(self, adv_data):
        return adv_data.rsi > self.rsi_high and adv_data.stoch_rsi > self.stoch_high and adv_data.money_flow_index > self.mfi_high

    def update_transaction_data(self, date):
        transactions = Transaction.objects.filter(algorithm=self, start_date=date, complete=False)
        for t in transactions:
            day_data = DayData.objects.get(ticker=t, day=DayData.objects.get(ticker=t, date=date).day + 1)
            if t.start_price is None:
                high, low = (t.initial_price * (1 + self.percent_tolerance)), (t.initial_price * (1 - self.percent_tolerance))
                start_price = self._get_start_price(day_data, high, low)
                if start_price is None:
                    t.delete()
                else:
                    t.start_price = start_price
                    t.save()
            elif day_data.low <= t.stop_loss:
                if day_data.open <= t.stop_loss:
                    t.end_price = day_data.open
                else:
                    t.end_price = t.stop_loss
                t.end_date = day_data.date
                t.complete = True
                t.save()
            elif day_data.high >= t.target:
                if day_data.open >= t.target:
                    t.end_price = day_data.open
                else:
                    t.end_price = t.target
                t.end_date = day_data.date
                t.complete = True
                t.save()
