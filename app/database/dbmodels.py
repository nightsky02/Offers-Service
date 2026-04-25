from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import VARCHAR, DECIMAL, UniqueConstraint, and_
import decimal

class Base(DeclarativeBase):
    pass


class DbOfferModel(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int]
    offer_id: Mapped[int]
    name: Mapped[str] = mapped_column(VARCHAR(100))
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    quantity: Mapped[int]
    avaivable: Mapped[bool]

    __table_args__ = (UniqueConstraint("seller_id", "offer_id"),)


    def __repr__(self):
        prop_values = []

        for prop_name in self.__table__.columns.keys():
            prop_values.append(f"{prop_name}={getattr(self, prop_name)}")

        return f"DbOfferModel({', '.join(prop_values)})"


class DbProcessResult:
    def __init__(self):
        self.success_count = 0
        self.updated_count = 0
        self.deleted_count = 0


class SearchConditionBuilder:
    def __init__(self):
        self.__condition = []
    
    def seller(self, seller_id: int | None):
        if seller_id:
            self.__condition.append(DbOfferModel.seller_id == seller_id)
        return self

    def offer(self, offer_id: int | None):
        if offer_id:
            self.__condition.append(DbOfferModel.offer_id == offer_id)
        return self
    
    def title(self, name: str | None):
        if name:
            self.__condition.append(DbOfferModel.name.contains(name))
        return self
    
    def compile(self):
        if len(self.__condition) == 0:
            return None
        elif len(self.__condition) == 1:
            return self.__condition[0]
        else:
            return and_(*self.__condition)         