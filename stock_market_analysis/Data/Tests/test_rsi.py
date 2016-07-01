from django.test import TestCase
from stock_market_analysis.Data.models import AdvancedStats


class RSITestCase(TestCase):

    def test_legit_rsi(self):
        adv = AdvancedStats.objects.all()
        for a in adv:
            if a.rsi is None:
                pass
            else:
                self.assertTrue(0 <= a.rsi <= 100)
