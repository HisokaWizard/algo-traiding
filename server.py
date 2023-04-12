from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.excanges_connector.sandbox_tinkoff import set_candle_price_to_share, get_shares_list, \
    shares
from src.excanges_connector.shares_item import SharesItem, count_actual_trend_by_year, count_summary_trend

# Run server command: uvicorn server:app --host 127.0.0.1 --port 5005 --reload
app = FastAPI(
    title='TradingBot',
)

origins = [
    "http://localhost:5005",
    "http://localhost:5004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def base_answer():
    return 'Correct server working'


@app.get('/shares', response_model=List[SharesItem])
def get_shares(country_code: str):
    return get_shares_list(country_code)


@app.get('/share/{ticker}', response_model=SharesItem)
def get_price(ticker: str, days_ago: int, country_code: str):
    if len(shares) == 0:
        get_shares(country_code)
    share: SharesItem = list(filter(lambda sh: sh.ticker == ticker, shares))[0]
    set_candle_price_to_share(share, days_ago)
    return share


@app.post('/shares_by_tickers', response_model=List[SharesItem])
def get_prices_by_tickers(tickers: List[str], attention: float, country_code: str):
    if len(shares) == 0:
        get_shares(country_code)
    shares_by_tickers: List[SharesItem] = list(filter(lambda sh: sh.ticker in tickers, shares))
    for share in shares_by_tickers:
        set_candle_price_to_share(share, 0)
        set_candle_price_to_share(share, 7)
        set_candle_price_to_share(share, 30)
        set_candle_price_to_share(share, 90)
        set_candle_price_to_share(share, 180)
        set_candle_price_to_share(share, 365)
        # trend counting
        _attention1 = count_actual_trend_by_year(share.year_ago_price, share.today_price, share.actual_trend_year,
                                                 attention)
        _attention2 = count_actual_trend_by_year(share.half_year_ago_price, share.today_price,
                                                 share.actual_trend_half_year,
                                                 attention)
        _attention3 = count_actual_trend_by_year(share.three_month_ago_price, share.today_price,
                                                 share.actual_trend_three_months,
                                                 attention)
        _attention4 = count_actual_trend_by_year(share.month_ago_price, share.today_price, share.actual_trend_month,
                                                 attention)
        _attention5 = count_actual_trend_by_year(share.week_ago_price, share.today_price, share.actual_trend_week,
                                                 attention)
        count_summary_trend(share, attention)
        if share.strong_attention or _attention1 or _attention2 or _attention3 or _attention4 or _attention5:
            share.strong_attention = True
    return shares_by_tickers
