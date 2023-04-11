from datetime import datetime, timedelta
from enum import Enum

from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import now

from src.excanges_connector.shares_item import SharesItem


def select_only_work_day(day: datetime) -> datetime:
    if day.weekday() == 5:
        return day - timedelta(days=1)
    if day.weekday() == 6:
        return day - timedelta(days=2)
    return day


class WatchedDays(Enum):
    DAY = 0
    WEEK = 7
    MONTH = 30
    THREE_MONTH = 90
    HALF_YEAR = 180
    YEAR = 365


def get_period_and_interval(from_: int):
    from_period = select_only_work_day(now() - timedelta(days=from_ + 1))
    to_period = from_period + timedelta(days=1)
    interval_hour = CandleInterval.CANDLE_INTERVAL_HOUR
    return from_period, to_period, interval_hour


def select_middle_share_amount(share: SharesItem, amount: float, from_: int):
    if from_ == WatchedDays.DAY.value:
        share.today_price = amount
    if from_ == WatchedDays.WEEK.value:
        share.week_ago_price = amount
    if from_ == WatchedDays.MONTH.value:
        share.month_ago_price = amount
    if from_ == WatchedDays.THREE_MONTH.value:
        share.three_month_ago_price = amount
    if from_ == WatchedDays.HALF_YEAR.value:
        share.half_year_ago_price = amount
    if from_ == WatchedDays.YEAR.value:
        share.year_ago_price = amount
