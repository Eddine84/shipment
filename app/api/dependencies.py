from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.serller import SellerService
from app.service.shipment import ShipmentService
from app.database.session import get_session

# session de puis session.py
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# fonction qui prend session comme parametre et insteci la class Shipment service qui comminique avec db er retourne un einsence
def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)


ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]


def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
