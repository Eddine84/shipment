from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.shipment import ShipmentService
from app.database.session import get_session

SessionDep = Annotated[AsyncSession,Depends(get_session)]

def get_shipment_service(session:SessionDep)->ShipmentService:
    return ShipmentService(session)



ServiceDep =  Annotated[ShipmentService,Depends(get_shipment_service)]