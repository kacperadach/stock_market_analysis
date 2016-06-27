from stock_market_analysis.Data.Tickers import Tickers

for t in Tickers.get_all_tickers():
    print(t)