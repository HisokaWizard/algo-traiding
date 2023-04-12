from pydantic import BaseModel


class Trend(BaseModel):
    trend: bool
    power: float


class SharesItem(BaseModel):
    id: str = None
    ticker: str = None
    name: str = None
    figi: str = None
    lot: int = None
    year_ago_price: float = None
    half_year_ago_price: float = None
    three_month_ago_price: float = None
    month_ago_price: float = None
    week_ago_price: float = None
    today_price: float = None
    currency: str = None
    strong_attention: bool = False
    country_of_risk: str = None
    country_of_risk_name: str = None

    actual_trend_year: Trend = Trend(trend=False, power=0)
    actual_trend_half_year: Trend = Trend(trend=False, power=0)
    actual_trend_three_months: Trend = Trend(trend=False, power=0)
    actual_trend_month: Trend = Trend(trend=False, power=0)
    actual_trend_week: Trend = Trend(trend=False, power=0)
    summary_trend_by_year: Trend = Trend(trend=False, power=0)

    def __str__(self):
        return 'Share: ' + self.ticker + ':' + self.name + ', id: ' + self.id + ' figi: ' + self.figi + ', lots: ' \
            + str(self.lot) + ', currency: ' + self.currency + ', prices (y/hy/3m/m/w/d): ' \
            + str(self.year_ago_price) + '/' + str(self.half_year_ago_price) + '/' \
            + str(self.three_month_ago_price) + '/' + str(self.month_ago_price) + '/' + str(self.week_ago_price) + '/' \
            + str(self.today_price)


def count_summary_trend(share: SharesItem, attention: float):
    if share.actual_trend_year is not None \
            and share.actual_trend_half_year is not None \
            and share.three_month_ago_price is not None \
            and share.month_ago_price is not None \
            and share.actual_trend_week is not None:
        share.summary_trend_by_year.power = (share.actual_trend_year.power + share.actual_trend_half_year.power +
                                             share.actual_trend_three_months.power + share.actual_trend_month.power +
                                             share.actual_trend_week.power) / 5
        if share.summary_trend_by_year.power > 0:
            share.summary_trend_by_year.trend = True
        else:
            share.summary_trend_by_year.trend = False
    if share.summary_trend_by_year.power > attention or share.summary_trend_by_year.power < -attention:
        share.strong_attention = True


def count_actual_trend_by_year(ago_price: float, today_price: float, actual_trend: Trend, attention: float):
    if ago_price is not None and today_price is not None:
        middle_sum = (ago_price + today_price) / 2
        if middle_sum > today_price:
            actual_trend.trend = False
            actual_trend.power = -(ago_price * 100 / today_price) + 100
        else:
            actual_trend.trend = True
            actual_trend.power = 100 - (ago_price * 100 / today_price)
    if actual_trend.power > attention or actual_trend.power < -attention:
        return True
    return False
