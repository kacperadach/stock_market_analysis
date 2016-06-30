from django.contrib import admin
from models import *

class StockDataInline(admin.TabularInline):
    model = DayData
    verbose_name = 'Daily Stock Data'

class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'market_cap', 'average_volume', 'eps', 'short_ratio', 'pe', 'peg')
    inlines = [
        StockDataInline,
    ]
    ordering = ('ticker',)
    search_fields = ['ticker']

admin.site.register(Stock, StockAdmin)
