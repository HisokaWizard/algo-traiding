from pydantic import BaseModel


class Share(BaseModel):
    id: str = None
    ticker: str = None
    name: str = None
    figi: str = None
    lot: int = None
    currency: str = None
    country_of_risk: str = None
    country_of_risk_name: str = None

    def __str__(self):
        return 'Share: ' + self.ticker + ':' + self.name + ', id: ' + self.id + ' figi: ' + self.figi + ', lots: ' \
            + str(self.lot) + ', currency: ' + self.currency
