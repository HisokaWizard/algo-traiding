from datetime import datetime, timedelta
from enum import Enum

from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import now

from src.excanges_connector.share_quotation import ShareQuotation


def select_only_work_day(day: datetime) -> datetime:
    time = now().time().hour.real
    if day.weekday() == 4 and time > 12 or day.weekday() == 5 and time < 12:
        return day - timedelta(days=1)
    if day.weekday() == 5 and time > 12 or day.weekday() == 6 and time < 12:
        return day - timedelta(days=2)
    if day.weekday() == 6 and time > 12:
        return day - timedelta(days=3)
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


def select_middle_share_amount(share_quotation: ShareQuotation, amount: float, from_: int):
    if from_ == WatchedDays.DAY.value:
        share_quotation.today_price = amount
    if from_ == WatchedDays.WEEK.value:
        share_quotation.week_ago_price = amount
    if from_ == WatchedDays.MONTH.value:
        share_quotation.month_ago_price = amount
    if from_ == WatchedDays.THREE_MONTH.value:
        share_quotation.three_month_ago_price = amount
    if from_ == WatchedDays.HALF_YEAR.value:
        share_quotation.half_year_ago_price = amount
    if from_ == WatchedDays.YEAR.value:
        share_quotation.year_ago_price = amount
