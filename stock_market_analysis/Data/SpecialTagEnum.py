from enum import Enum


class SpecialTag(Enum):

    ask = 'a'
    avg_daily_vol = 'a2'
    ask_size = 'a5'
    bid = 'b'
    ask_rt = 'b2'
    bid_rt = 'b3'
    book_value = 'b4'
    bid_size = 'b6'
    change_pct_change = 'c1'
    commission = 'c3'
    change_rt = 'c6'
    ah_change_rt = 'c8'
    dividend = 'd'
    last_trade_date = 'd1'
    trade_date = 'd2'
    eps = 'e'
    error_indication = 'e1'
    eps_est_cur_year = 'e7'
    eps_est_nxt_year = 'e8'
    eps_est_nxt_qrt = 'e9'
    float_shares = 'f6'
    day_low = 'g'
    day_high = 'h'
    fifty_two_week_low = 'j'
    fifty_two_week_high = 'k'
    more_info = 'i'
    order_book_rt = 'i5'
    market_cap = 'j1'
    market_cap_rt = 'j3'
    ebitda = 'j4'
    change_from_low = 'j5'
    pct_change_from_low = 'j6'
    last_trade_rt = 'k1'
    change_pct_rt = 'k2'
    last_trade_size = 'k3'
    change_from_high = 'k4'
    pct_change_from_high = 'k5'
    last_trade = 'l1'
    high_limit = 'l2'
    low_limit = 'l3'
    day_range = 'm'
    day_range_rt = 'm2'
    fifty_MA = 'm3'
    two_hundred_MA = 'm4'
    change_from_thdMA = 'm5'
    pct_change_from_thdMA = 'm6'
    change_from_fdMA = 'm7'
    pct_change_from_fdMA = 'm8'
    name = 'n'
    open = 'o'
    previous_close = 'p'
    pct_change = 'p2'
    price_sales = 'p5'
    price_book = 'p6'
    ex_div_date = 'q'
    pe = 'r'
    dividend_pay_date = 'r1'
    pe_rt = 'r2'
    peg = 'r5'
    price_eps_est_cur_year = 'r6'
    price_eps_est_nxt_year = 'r7'
    symbol = 's'
    shares_owned = 's1'
    short_ratio = 's7'
    last_trade_time = 't1'
    trade_links = 't6'
    ticker_trend = 't7'
    one_yr_target = 't8'
    volume = 'v'
    fifty_two_week_range = 'w'
    day_value_change = 'w1'
    day_value_change_rt = 'w4'
    stock_exchange = 'x'
    dividend_yield = 'y'

    @staticmethod
    def get_string(tag):
        return tag.value











