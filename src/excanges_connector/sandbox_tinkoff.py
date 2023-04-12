from decimal import Decimal

from tinkoff.invest import MoneyValue, OpenSandboxAccountResponse, GetAccountsResponse, \
    SandboxPayInResponse
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import decimal_to_quotation

from src.excanges_connector.shares_item import SharesItem
from src.excanges_connector.token_loader_tinkoff import token_loader
from src.excanges_connector.utils import get_period_and_interval, select_middle_share_amount

TOKEN = token_loader()


def create_account() -> OpenSandboxAccountResponse:
    with SandboxClient(TOKEN) as client:
        return client.sandbox.open_sandbox_account()


def get_accounts() -> GetAccountsResponse:
    with SandboxClient(TOKEN) as client:
        return client.sandbox.get_sandbox_accounts()


def remove_account(account_id):
    with SandboxClient(TOKEN) as client:
        client.sandbox.close_sandbox_account(account_id=account_id)


def add_cash_to_account(account_id, amount) -> SandboxPayInResponse:
    with SandboxClient(TOKEN) as client:
        quotation = decimal_to_quotation(Decimal(amount))
        money = MoneyValue(units=quotation.units, nano=quotation.nano, currency='rub')
        balance = client.sandbox.sandbox_pay_in(account_id=account_id, amount=money)
    return balance


def get_balance(account_id) -> MoneyValue:
    with SandboxClient(TOKEN) as client:
        portfolio = client.sandbox.get_sandbox_portfolio(account_id=account_id)
    return portfolio.total_amount_currencies


def set_candle_price_to_share(share: SharesItem, from_: int):
    with SandboxClient(TOKEN) as client:
        (from_period, to_period, interval_hour) = get_period_and_interval(from_)
        nano_scale = 1000000000
        counter = 0
        candle_amount_units_sum = 0
        candle_amount_nano_sum = 0
        for candle in client.get_all_candles(from_=from_period, to=to_period, interval=interval_hour,
                                             figi=share.figi):
            if candle:
                counter += 1
                candle_amount_units_sum += candle.close.units
                candle_amount_nano_sum += candle.close.nano / nano_scale
        if counter != 0:
            candle_amount_units = candle_amount_units_sum / counter
            candle_amount_nano = candle_amount_nano_sum / counter
            amount: float = round(candle_amount_units + candle_amount_nano, 4)
            select_middle_share_amount(share=share, amount=amount, from_=from_)


shares = []


def get_shares_list(country_code: str) -> list[SharesItem]:
    with SandboxClient(TOKEN) as client:
        all_shares = client.instruments.shares()
        shares.clear()
        for instrument in all_shares.instruments:
            if instrument.country_of_risk != country_code:
                continue
            share_item = SharesItem()
            share_item.id = instrument.uid
            share_item.ticker = instrument.ticker
            share_item.figi = instrument.figi
            share_item.name = instrument.name
            share_item.lot = instrument.lot
            share_item.currency = instrument.currency
            share_item.country_of_risk = instrument.country_of_risk
            share_item.country_of_risk_name = instrument.country_of_risk_name
            shares.append(share_item)
        return shares
