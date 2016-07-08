from django.core.management.base import BaseCommand
from stock_market_analysis.Data.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Stock.objects.all().delete()
        # DayData.objects.all().delete()
        AdvancedStats.objects.all().delete()
