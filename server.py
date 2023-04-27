from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.excanges_connector.sandbox_tinkoff import get_candle_price_to_share, get_shares_list, \
    get_country_tickers_and_figi
from src.excanges_connector.share import Share
from src.excanges_connector.share_quotation import ShareQuotation, count_actual_trend_by_period, count_summary_trend
from src.excanges_connector.share_ticker import ShareTicker

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


@app.get('/share_tickers', response_model=List[ShareTicker])
def get_share_tickers(country_code: str):
    return get_country_tickers_and_figi(country_code)


@app.get('/shares', response_model=List[Share])
def get_shares(country_code: str):
    return get_shares_list(country_code)


@app.get('/shares_by_tickers', response_model=ShareQuotation)
def get_prices_by_ticker(ticker: str, figi: str, attention: float):
    share_quotation = ShareQuotation()
    share_quotation.ticker = ticker
    get_candle_price_to_share(share_quotation, figi, 0)
    get_candle_price_to_share(share_quotation, figi, 7)
    get_candle_price_to_share(share_quotation, figi, 30)
    get_candle_price_to_share(share_quotation, figi, 90)
    get_candle_price_to_share(share_quotation, figi, 180)
    get_candle_price_to_share(share_quotation, figi, 365)
    get_candle_price_to_share(share_quotation, figi, 730)
    get_candle_price_to_share(share_quotation, figi, 1095)

    today_price = share_quotation.today_price
    years_three_ago_price = share_quotation.three_years_ago_price
    years_two_ago_price = share_quotation.two_years_ago_price
    year_ago_price = share_quotation.year_ago_price
    half_year_ago_price = share_quotation.half_year_ago_price
    three_month_ago_price = share_quotation.three_month_ago_price
    month_ago_price = share_quotation.month_ago_price
    week_ago_price = share_quotation.week_ago_price
    trend_three_years = share_quotation.actual_trend_three_years
    trend_two_years = share_quotation.actual_trend_two_years
    trend_year = share_quotation.actual_trend_year
    trend_half_year = share_quotation.actual_trend_half_year
    trend_three_months = share_quotation.actual_trend_three_months
    trend_month = share_quotation.actual_trend_month
    trend_week = share_quotation.actual_trend_week

    attention1 = count_actual_trend_by_period(years_three_ago_price, today_price, trend_three_years, attention)
    attention2 = count_actual_trend_by_period(years_two_ago_price, today_price, trend_two_years, attention)
    attention3 = count_actual_trend_by_period(year_ago_price, today_price, trend_year, attention)
    attention4 = count_actual_trend_by_period(half_year_ago_price, today_price, trend_half_year, attention)
    attention5 = count_actual_trend_by_period(three_month_ago_price, today_price, trend_three_months, attention)
    attention6 = count_actual_trend_by_period(month_ago_price, today_price, trend_month, attention)
    attention7 = count_actual_trend_by_period(week_ago_price, today_price, trend_week, attention)
    count_summary_trend(share_quotation, attention)

    if share_quotation.strong_attention or attention1 or attention2 or attention3 or \
            attention4 or attention5 or attention6 or attention7:
        share_quotation.strong_attention = True
    return share_quotation
