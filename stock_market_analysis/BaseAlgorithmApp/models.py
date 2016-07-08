from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from stock_market_analysis.Data.models import AdvancedStats

ORDER_CHOICES = (
    (0, 'long'),
    (1, 'short')
)


class Algorithm(models.Model):

    name = models.CharField(max_length=50, blank=False)

    class Meta:
        abstract = True

    def create_transaction(self, type, stock, initial_price, start_date):
        transactions = Transaction.objects.filter(algorithm=self, stock=stock)
        for t in transactions:
            if not t.complete:
                return
        Transaction.objects.create(algorithm=self, type=type, stock=stock, initial_price=initial_price, start_date=start_date)

    def get_overall_return(self):
        transactions = Transaction.objects.filter(algorithm=self)
        total_ret = 0
        for t in transactions:
            if t.complete:
                total_ret += t.get_percent_return()
        return total_ret

    def delete_all_incomplete_transactions(self):
        all_transactions = Transaction.objects.filter(algorithm=self)
        for t in all_transactions:
            if t.complete is False:
                t.delete()

    def _in_float_range(self, num, high, low):
        return  low <= num <= high

    def _get_start_price(self, data, high, low):
        if self._in_float_range(data.open, high, low):
            return data.open
        else:
            if data.open > high:
                if self._in_float_range(data.low, high, low):
                    return high
                else:
                    if data.low > high:
                        return None
                    else:
                        return high
            else:
                if self._in_float_range(data.high, high, low):
                    return low
                else:
                    if data.high < low:
                        return None
                    else:
                        return low

    def run(self, data):
        verdict = self.filter(AdvancedStats.objects.get(data=data))
        if verdict == -1:
            return
        else:
            self.create_transaction(verdict, data.ticker, data.close, data.date)

    def filter(self, adv_data):
        if self.go_long(adv_data):
            return 0
        elif self.go_short(adv_data):
            return 1
        else:
            return -1


class Transaction(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    algorithm = GenericForeignKey('content_type', 'object_id')
    type = models.IntegerField(choices=ORDER_CHOICES)
    stock = models.ForeignKey('Data.Stock')
    complete = models.BooleanField(default=False)
    stop_loss = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    target = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    initial_price = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    start_price = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    start_date = models.DateField(blank=False)
    end_price = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)
    end_date = models.DateField(blank=True, null=True)

    @classmethod
    def create(cls, algorithm, type, stock, initial_price, stop_loss, target, start_date):
        return cls(algorithm=algorithm,
                   type=type,
                   stock=stock,
                   initial_price=initial_price,
                   stop_loss=stop_loss,
                   target=target,
                   start_date=start_date,)

    def _get_all_attributes(self):
        return [self.start_price, self.end_price, self.end_date]

    def incomplete_transaction(self):
        for var in self._get_all_attributes():
            if var is None:
                return True
        return False

    def get_percent_return(self):
        if self.complete:
            per_ret = ((self.end_price - self.start_price) / self.start_price) * 100
            if self.type == 0:
                return per_ret
            else:
                return per_ret * -1

