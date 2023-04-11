from fastapi import FastAPI

from src.excanges_connector.sandbox_tinkoff import get_ru_shares_list, set_candle_price_to_share
from src.excanges_connector.shares_item import SharesItem

# Run server command: uvicorn server:app --host 127.0.0.1 --port 5005 --reload
app = FastAPI(
    title='TradingBot',
)

ru_shares: list[SharesItem] = []


@app.get('/')
def base_answer():
    return 'Correct server working'


@app.get('/ru_shares')
def get_ru_shares():
    shares: list[SharesItem] = get_ru_shares_list()
    for share in shares:
        ru_shares.append(share)
    return ru_shares


@app.get('/ru_shares/{ticker}')
def get_price(ticker: str, days_ago: int):
    share: SharesItem = list(filter(lambda sh: sh.ticker == ticker, ru_shares))[0]
    set_candle_price_to_share(share, days_ago)
    return share
