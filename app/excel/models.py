from pydantic import BaseModel, Field, field_validator
from typing import NamedTuple
import decimal

class OfferDataModel(BaseModel):
    offer_id: int = Field(ge=0)
    name: str = Field(min_length=1, max_length=100)
    price: decimal.Decimal = Field(ge=0)
    quantity: int = Field(ge=0)
    avaivable: bool


    @field_validator("price", mode="before")
    @classmethod
    def parse_price(cls, v: str) -> str:
        clear_price: str = v
        if isinstance(v, str):
            clear_price = clear_price.replace(" ", "").replace(",", ".")
        return clear_price


class OfferDTO(OfferDataModel):
    seller_id: int = Field(ge=0)

class WrongOfferModel(BaseModel):
    offer_id: int
    err_msg: str


class OfferParsingResult(NamedTuple):
    correct_offers: list[OfferDataModel]
    wrong_offers: list[WrongOfferModel]


