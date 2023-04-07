from datetime import timedelta
from decimal import Decimal

from tinkoff.invest import MoneyValue, CandleInterval
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import decimal_to_quotation, now

from src.sandbox.token_loader import token_loader

TOKEN = token_loader()
my_tickers = {'SBER': 'SBER', 'VKCO': 'VKCO', 'GAZP': 'GAZP', 'RTKM': 'RTKM', 'YNDX': 'YNDX'}


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


def add_my_shares_list(client, tickers):
    all_shares = client.instruments.shares()
    my_shares = list(filter(lambda it: it.ticker == tickers.get(it.ticker), all_shares.instruments))
    return tuple(map(
        lambda item: {'ticker': item.ticker, 'class_code': item.class_code, 'lot': item.lot,
                      'currency': item.currency, 'name': item.name, 'exchange': item.exchange,
                      'issue_size_plan': item.issue_size_plan, 'uid': item.uid, 'figi': item.figi}, my_shares))


def get_candles_by_week(client, figi):
    return client.get_all_candles(from_=now() - timedelta(days=2), interval=CandleInterval.CANDLE_INTERVAL_HOUR,
                                  figi=figi)


def create_order_to_buy(client):
    return None


def sandbox():
    with SandboxClient(TOKEN) as client:
        accounts = client.sandbox.get_sandbox_accounts()
        for acc in accounts.accounts:
            client.sandbox.close_sandbox_account(account_id=acc.id)
        # Create new account for sandbox and set 1000000
        # (account_id, balance) = create_account_with_currencies(client, 1000000)
        # print('Balance:', balance)
        # print('Account id:', account_id)
        # # Add interesting for me shares to the specific prepared list
        # my_shares_data = add_my_shares_list(client, my_tickers)
        # count = 0
        # for it in my_shares_data:
        #     count += 1
        #     print('Item ' + str(count) + ':', it)
        # print('-----' * 10 + '\n')
        # candles_vk = get_candles_by_week(client, my_shares_data[0]['figi'])
        # for candle in candles_vk:
        #     print(candle)
        #
        # price = Quotation(units=0, nano=0)
        # direction = OrderDirection.ORDER_DIRECTION_BUY
        # order_type = OrderType.ORDER_TYPE_MARKET
        # print(my_shares_data[0]['name'])
        # order_result = client.sandbox.post_sandbox_order(figi=my_shares_data[0]['figi'], quantity=100,
        #                                                  account_id=account_id, direction=direction,
        #                                                  order_type=order_type,
        #                                                  instrument_id=my_shares_data[0]['uid'])
        # print(order_result)
        # my_profile = client.sandbox.get_sandbox_portfolio(account_id=account_id)
        # print(my_profile)
