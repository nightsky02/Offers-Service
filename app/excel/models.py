from pydantic import BaseModel, Field
from typing import NamedTuple
import decimal

class OfferDataModel(BaseModel):
    offer_id: int = Field(ge=0)
    name: str = Field(min_length=1, max_length=100)
    price: decimal.Decimal = Field(ge=0)
    quantity: int = Field(ge=0)
    avaivable: bool


class OfferDTO(OfferDataModel):
    seller_id: int = Field(ge=0)

class WrongOfferModel(BaseModel):
    offer_id: int
    err_msg: str


class OfferParsingResult(NamedTuple):
    correct_offers: list[OfferDataModel]
    wrong_offers: list[WrongOfferModel]


