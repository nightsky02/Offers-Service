from app.database.dbmodels import OfferModel, Base
from app.database.init import session_fabric, engine
from sqlalchemy import select, update
from app.database.api import get_seller_products

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
 
# with session_fabric() as session:
#     obj = OfferModel(
#         seller_id=2,
#         offer_id=2,
#         name="Мышка",
#         price=43.23,
#         quantity=50,
#         avaivable=True
#     )

#     query = select(OfferModel).filter_by(seller_id=2)
#     obj_second = session.execute(query).scalars().one()
#     obj_second.quantity = 51

#     session.commit()

get_seller_products(2)
# 2. Узнать, как обрабатывать ошибки, полученные от алхимии (ловить коды, состояния...)