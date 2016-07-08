from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from models import *


class AdvancedDataInline(NestedStackedInline):
    model = AdvancedStats
    max_num = 10


class StockDataInline(NestedStackedInline):
    model = DayData
    extra = 1
    verbose_name = 'Daily Stock Data'
    inlines = [AdvancedDataInline]
    ordering = ('-day',)
    max_num = 10


class StockAdmin(NestedModelAdmin):
    model = Stock
    list_display = ('ticker', 'market_cap', 'average_volume', 'eps', 'short_ratio', 'pe', 'peg')
    inlines = [
        StockDataInline,
    ]
    ordering = ('ticker',)
    search_fields = ['ticker']

admin.site.register(Stock, StockAdmin)
