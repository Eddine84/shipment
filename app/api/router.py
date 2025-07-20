from fastapi import APIRouter
from .routers import seller
from .routers import shipment


master_router = APIRouter()


master_router.include_router(seller.router)
master_router.include_router(shipment.router)
