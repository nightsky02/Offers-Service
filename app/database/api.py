from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.database.dbmodels import DbOfferModel, DbProcessResult, SearchConditionBuilder
from app.database.init import session_fabric
from app.excel.models import OfferDataModel, OfferDTO


def get_seller_products(seller_id: int, offers_models: list[OfferDataModel], session: Session) -> list[DbOfferModel] | None:
    """
        Returns necessary offers from database as a list of database offer models \n
        offers_models - a list of excel offer models
    """
    
    offers_ids = [model.offer_id for model in offers_models]

    query = (
        select(DbOfferModel)
        .where(and_(DbOfferModel.seller_id == seller_id, DbOfferModel.offer_id.in_(offers_ids)))
    )

    try:
        result = session.execute(query)
        return result.scalars().all()
    except:
        return None


def _extract_offer_from_list(ex_offer: OfferDataModel, db_offers: list[DbOfferModel]) -> DbOfferModel:
    """
        Look for the same offer in the list of database models \n
        ex_offer - excel offer model \n
        db_offers - list of database offer model
    """
    for offer in db_offers:
        if offer.offer_id == ex_offer.offer_id:
            return offer
    return None


def _update_offer(ex_offer: OfferDataModel, db_offer: DbOfferModel) -> bool:
    """
        Update database offer model using data from excel offer model \n
        Returns true if some changes have been applied
    """

    changed = False

    if ex_offer.price != db_offer.price:
        db_offer.price = ex_offer.price
        changed = True

    if ex_offer.quantity != db_offer.quantity:
        db_offer.quantity = ex_offer.quantity
        changed = True

    if ex_offer.avaivable != db_offer.avaivable:
        db_offer.avaivable = ex_offer.avaivable
        changed = True

    return changed


def process_offers(seller_id: int, offer_models: list[OfferDataModel]) -> DbProcessResult:
    """
        Processes offers for some seller (add, delete or update in the db) \n

        seller_id - Seller id \n
        offer_models - The list of excel offer models \n

        Returns the simple statistics of deleted, updated and added offers
    """


    with session_fabric() as session:
        contained_offers = get_seller_products(seller_id, offer_models, session)
        _proccess_counter = DbProcessResult()

        # look around all our recieved products, and try to find them in the collection
        # of the found products from db
        for offer in offer_models:
            db_offer = _extract_offer_from_list(offer, contained_offers)

            # case when offer doesn't exist in db
            if db_offer is None:
                if not offer.avaivable:
                    print(
                        f"The offer {offer.offer_id} has been skept because of unavaivable")
                    continue

                # push offer to the db
                session.add(DbOfferModel(
                    seller_id=seller_id,
                    **offer.model_dump()
                ))
                _proccess_counter.success_count += 1
                print(f"The offer {offer.offer_id} has been added into db")
            else:
                # case, when offer exists, but gonna be removed (avaivable = 0)
                if not offer.avaivable:
                    session.delete(db_offer)
                    print(f"The offer {offer.offer_id} has been deleted because of unavaivable")
                    _proccess_counter.deleted_count += 1
                    continue

                # otherwise, update our offer, if it wasn't removed and it was contained in db
                if _update_offer(offer, db_offer):
                    print(f"The offer {offer.offer_id} has been updated")
                    _proccess_counter.updated_count += 1
                else:
                    print(f"The offer {offer.offer_id} just be checked and get without changes.")

        session.commit()

        return _proccess_counter


def select_offers(seller_id: int, offer_id: int, name: str) -> list[OfferDTO]:

    condition = (SearchConditionBuilder()
                 .seller(seller_id)
                 .offer(offer_id)
                 .title(name)
                 .compile())

    if condition is None:
        return None
    
    basic_query = (
        select(DbOfferModel)
        .where(condition)
    )

    with session_fabric() as session:
        result = session.execute(basic_query)   
        db_offer_models = result.scalars().all()

        excel_offer_models = [
            OfferDTO.model_validate(model, from_attributes=True) for model in db_offer_models]
        
        return excel_offer_models
