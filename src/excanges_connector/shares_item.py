class SharesItem:
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

    def __init__(self, uid, ticker, name, figi, lot, currency):
        self.id = uid
        self.ticker = ticker
        self.figi = figi
        self.name = name
        self.lot = lot
        self.currency = currency

    def __str__(self):
        return 'Share: ' + self.ticker + ':' + self.name + ', id: ' + self.id + ' figi: ' + self.figi + ', lots: ' \
            + str(self.lot) + ', currency: ' + self.currency + ', prices (y/hy/3m/m/w/d): ' \
            + str(self.year_ago_price) + '/' + str(self.half_year_ago_price) + '/' \
            + str(self.three_month_ago_price) + '/' + str(self.month_ago_price) + '/' + str(self.week_ago_price) + '/' \
            + str(self.today_price)

    def add_price_pool_to_item(self, year, half_year, three_month, month, week, day):
        self.year_ago_price = year
        self.half_year_ago_price = half_year
        self.three_month_ago_price = three_month
        self.month_ago_price = month
        self.week_ago_price = week
        self.today_price = day
