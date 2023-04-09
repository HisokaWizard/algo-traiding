import datetime
from datetime import timedelta
from decimal import Decimal

from tinkoff.invest import MoneyValue, CandleInterval
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import decimal_to_quotation, now

from src.sandbox.token_loader import token_loader

TOKEN = token_loader()


def create_account():
    with SandboxClient(TOKEN) as client:
        account = client.sandbox.open_sandbox_account()
    return account


def get_accounts():
    with SandboxClient(TOKEN) as client:
        accounts = client.sandbox.get_sandbox_accounts()
    return accounts.accounts


def remove_account(account_id):
    with SandboxClient(TOKEN) as client:
        client.sandbox.close_sandbox_account(account_id=account_id)


def add_cash_to_account(account_id, amount):
    with SandboxClient(TOKEN) as client:
        quotation = decimal_to_quotation(Decimal(amount))
        money = MoneyValue(units=quotation.units, nano=quotation.nano, currency='rub')
        balance = client.sandbox.sandbox_pay_in(account_id=account_id, amount=money)
    return balance


def get_balance(account_id):
    with SandboxClient(TOKEN) as client:
        portfolio = client.sandbox.get_sandbox_portfolio(account_id=account_id)
    return portfolio.total_amount_currencies


class PriceKeys:
    YEAR = 'year_ago_price'
    HALF_YEAR = 'half_year_ago_price'
    THREE_MONTH = 'three_month_ago_price'
    MONTH = 'month_ago_price'
    WEEK = 'week_ago_price'
    TODAY = 'today_price'


class SharesItem:
    id = None
    ticker = None
    name = None
    figi = None
    lot = None
    year_ago_price = None
    half_year_ago_price = None
    three_month_ago_price = None
    month_ago_price = None
    week_ago_price = None
    today_price = None
    currency = None

    def __init__(self, uid, ticker, name, figi, lot, currency):
        self.id = uid
        self.ticker = ticker
        self.figi = figi
        self.name = name
        self.lot = lot
        self.currency = currency

    def add_price_pool_to_item(self, year, half_year, three_month, month, week, day):
        self.year_ago_price = year
        self.half_year_ago_price = half_year
        self.three_month_ago_price = three_month
        self.month_ago_price = month
        self.week_ago_price = week
        self.today_price = day


def select_only_work_day(day: datetime):
    if day.today().weekday() == 5:
        return day - timedelta(days=2)
    if day.today().weekday() == 6:
        return day - timedelta(days=3)
    return day


def set_candle_price_to_share(share: SharesItem, from_: int):
    with SandboxClient(TOKEN) as client:
        from_period = select_only_work_day(now() - timedelta(days=from_))
        to_period = from_period + timedelta(days=1)
        interval_hour = CandleInterval.CANDLE_INTERVAL_HOUR
        counter = 0
        candle_amount_units_sum = 0
        candle_amount_nano_sum = 0
        for candle in client.get_all_candles(from_=from_period, to=to_period, interval=interval_hour,
                                             figi=share.figi):
            if not candle:
                break
            counter += 1
            candle_amount_units_sum += candle.close.units
            candle_amount_nano_sum += candle.close.nano
        if counter == 0:
            return None
        candle_amount_units = candle_amount_units_sum / counter
        candle_amount_nano = candle_amount_nano_sum / counter
        result = str(round(candle_amount_units)) + ',' + str(candle_amount_nano)[0:2]
        if from_ == 0:
            share.today_price = result
        if from_ == 7:
            share.week_ago_price = result
        if from_ == 30:
            share.month_ago_price = result
        if from_ == 90:
            share.three_month_ago_price = result
        if from_ == 180:
            share.half_year_ago_price = result
        if from_ == 365:
            share.year_ago_price = result


def get_ru_shares_list():
    with SandboxClient(TOKEN) as client:
        all_shares = client.instruments.shares()
        ru_shares = []
        for instrument in all_shares.instruments:
            if instrument.country_of_risk != 'RU':
                continue
            share_item = SharesItem(uid=instrument.uid, ticker=instrument.ticker, figi=instrument.figi,
                                    name=instrument.name, lot=instrument.lot, currency=instrument.currency)
            ru_shares.append(share_item)
        for share in ru_shares:
            set_candle_price_to_share(share, 0)
        return ru_shares
