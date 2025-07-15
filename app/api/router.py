from typing import Any
from fastapi import APIRouter, HTTPException, status


from app.api.dependencies import ServiceDep, SessionDep
from app.database.models import Shipment

from app.api.schemas.shipment import ShipementRead, ShipementCreate, ShipementUpdate


from app.service.shipment import ShipmentService

router = APIRouter(prefix="/shipment", tags=["Shipment"])


# # #recuperer le dernier shipement de list
@router.get("/latest", response_model=ShipementRead)
async def get_latest_shipment(session: ServiceDep):
    return await session.get_latest()


# # recuperer le shipement selon id  ?
@router.get("/{id}", response_model=ShipementRead)
async def get_shipment(id: int, session: ServiceDep):
    shipment = await session.get(id)
    if shipment is None:
        raise HTTPException(
            detail="Given id doesn't exist!", status_code=status.HTTP_404_NOT_FOUND
        )

    return shipment


# # #ajouter un nouveau shipment attention status est founi par defaut donc j ajoute pas a mon Shipment schema
@router.post("/", response_model=ShipementRead)
async def submit_shipment(
    shipment: ShipementCreate,
    session: ServiceDep,
) -> Shipment:
    return await session.add(shipment)


# # #recupéré la valeur d'une clés shipment
@router.get("/field/{field}", response_model=dict)
async def get_shipment_field(
    id: int, field: str, session: ServiceDep
) -> dict[str, Any]:
    return await session.get_field(id, field)


@router.patch("/{id}", response_model=ShipementRead)
async def update_shipment(
    id: int, shipment_update: ShipementUpdate, session: ServiceDep
) -> Shipment:
    update_data = shipment_update.model_dump(exclude_none=True)
    if update_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="no data provided to update"
        )

    return await session.update(id, update_data)


# # #effacer un shipment
@router.delete("/{id}")
async def delete_shipment(id: int, session: ServiceDep) -> dict[str, Any]:
    shipment_id = await session.delete(id)
    return {"id": shipment_id, "msg": "deleted"}
