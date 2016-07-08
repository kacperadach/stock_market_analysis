import datetime

from django.test import TestCase
from stock_market_analysis.Data.models import Stock, DayData, AdvancedStats


class DayDataTestCase(TestCase):

    def test_properly_ordered_day_data(self):
        stock = Stock.objects.get(ticker='WLL')  #find way to randomize stock
        dd = DayData.objects.filter(ticker=stock).order_by('day')
        for d in dd:
            if d.day == 0:
                date = d.date
            else:
                self.assertTrue(d.date > date)
                self.assertTrue(d.date.isoweekday() < 6)
                date = d.date
