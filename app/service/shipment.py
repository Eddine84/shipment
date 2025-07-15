from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas import shipment
from app.api.schemas.shipment import ShipementCreate, ShipementUpdate
from app.database.models import Shipment, ShipmentStatus
from typing import Any
from sqlmodel import select


class ShipmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> Shipment | None:
        return await self.session.get(Shipment, id)

    async def get_field(self, id: int, field: str) -> dict[str, Any]:
        stmt = select(Shipment).where(Shipment.id == id)
        result = await self.session.execute(stmt)
        shipment = result.scalars().first()
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )

        if not hasattr(shipment, field):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Field not in Shipment"
            )

        return {field: getattr(shipment, field)}

    async def get_latest(self) -> Shipment:
        stmt = select(Shipment).order_by(Shipment.id.desc())  # type: ignore
        result = await self.session.execute(stmt)
        shipment = result.scalars().first()
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not shipment found"
            )
        return shipment

    async def add(self, shipment: ShipementCreate) -> Shipment:
        shipment_to_senf = Shipment(
            **shipment.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
        )
        self.session.add(shipment_to_senf)
        await self.session.commit()
        await self.session.refresh(shipment_to_senf)
        return shipment_to_senf

    async def update(self, id: int, update_data: dict) -> Shipment:
        # je recuperer la valeur en dictionnaire au lieu de objet pydantic

        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="given id dot not exists"
            )
        shipment.sqlmodel_update(update_data)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, id: int) -> int:
        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="shipment do not exsite the the given id",
            )
        await self.session.delete(shipment)
        await self.session.commit()
        return id
