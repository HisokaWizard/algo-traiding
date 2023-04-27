from pydantic import BaseModel


class Trend(BaseModel):
    trend: bool
    power: float


class ShareQuotation(BaseModel):
    ticker: str = None
    three_years_ago_price: float = None
    two_years_ago_price: float = None
    year_ago_price: float = None
    half_year_ago_price: float = None
    three_month_ago_price: float = None
    month_ago_price: float = None
    week_ago_price: float = None
    today_price: float = None
    strong_attention: bool = False
    actual_trend_three_years: Trend = Trend(trend=False, power=0)
    actual_trend_two_years: Trend = Trend(trend=False, power=0)
    actual_trend_year: Trend = Trend(trend=False, power=0)
    actual_trend_half_year: Trend = Trend(trend=False, power=0)
    actual_trend_three_months: Trend = Trend(trend=False, power=0)
    actual_trend_month: Trend = Trend(trend=False, power=0)
    actual_trend_week: Trend = Trend(trend=False, power=0)
    summary_trend_by_year: Trend = Trend(trend=False, power=0)


def count_summary_trend(share_quotation: ShareQuotation, attention: float):
    trend_years_3 = share_quotation.actual_trend_three_years
    trend_years_2 = share_quotation.actual_trend_two_years
    trend_year = share_quotation.actual_trend_year
    trend_half_year = share_quotation.actual_trend_half_year
    trend_months_3 = share_quotation.actual_trend_three_months
    trend_month = share_quotation.actual_trend_month
    trend_week = share_quotation.actual_trend_week
    share_quotation.summary_trend_by_year.power = (trend_years_3.power + trend_years_2.power + trend_year.power +
                                                   trend_half_year.power + trend_months_3.power + trend_month.power +
                                                   trend_week.power) / 7
    if share_quotation.summary_trend_by_year.power > 0:
        share_quotation.summary_trend_by_year.trend = True
    else:
        share_quotation.summary_trend_by_year.trend = False
    if share_quotation.summary_trend_by_year.power > attention or share_quotation.summary_trend_by_year.power < -attention:
        share_quotation.strong_attention = True


def count_actual_trend_by_period(period_price: float, today_price: float, trend: Trend, attention: float):
    if period_price is not None and today_price is not None:
        middle_sum = (period_price + today_price) / 2
        if middle_sum > today_price:
            trend.trend = False
            trend.power = -(period_price * 100 / today_price) + 100
        else:
            trend.trend = True
            trend.power = 100 - (period_price * 100 / today_price)
    if trend.power > attention or trend.power < -attention:
        return True
    return False
