from pydantic import BaseModel


class ShareTicker(BaseModel):
    ticker: str = None
    figi: str = None
    id: str = None
