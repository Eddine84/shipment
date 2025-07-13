from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException,status


from app.api.schemas import shipment
from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep
from app.api.schemas.shipment import ShipementRead,ShipementCreate,ShipementUpdate

from sqlmodel import select

router = APIRouter()



# # #recuperer le dernier shipement de list
@router.get('/shipment/latest',response_model=ShipementRead)
async def get_latest_shipment(session:SessionDep):
    stmt = select(Shipment).order_by(Shipment.id.desc()) # type: ignore
    result = await session.execute(stmt)
    shipment =  result.scalars().first()
    if shipment is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not shipment found")
    return shipment


# # recuperer le shipement selon id 
@router.get('/shipment/{id}',response_model=ShipementRead)
async def get_shipment(id:int , session:SessionDep):
    shipment = await session.get(Shipment,id)
    if shipment is None:
       raise HTTPException(
        detail="Given id doesn't exist!",
        status_code=status.HTTP_404_NOT_FOUND
       )
      

    return shipment


# # #ajouter un nouveau shipment attention status est founi par defaut donc j ajoute pas a mon Shipment schema
@router.post('/shipment',response_model=None)
async def submit_shipment( shipment:ShipementCreate, session:SessionDep)->dict[str,int]:

    shipment_to_senf =  Shipment(**shipment.model_dump(),status=ShipmentStatus.placed, estimated_delivery=datetime.now() + timedelta(days=3))
    session.add(shipment_to_senf)
    await session.commit()
    await session.refresh(shipment_to_senf)
    return {"id":shipment_to_senf.id}



# # #recupéré la valeur d'une clés shipment
@router.get('/shipment/field/{field}', response_model=dict)
async def get_shipment_field(id: int, field: str, session: SessionDep) -> dict[str, any]:
    stmt = select(Shipment).where(Shipment.id == id)
    result = await session.execute(stmt)
    shipment = result.scalars().first()

    if shipment is None:
        raise HTTPException(404, "Shipment not found")


    if not hasattr(shipment, field):
        raise HTTPException(404, "Field not in Shipment")

    return {field: getattr(shipment, field)}







@router.patch('/shipment/{id}', response_model=ShipementRead )
async def update_shipment(id:int,shipment_update:ShipementUpdate , session:SessionDep) :

    #1 - je converti mon objet schema Basemodel en dictionnaire et retir les valeur non fourni
    update_data = shipment_update.model_dump(exclude_none=True)
    if update_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no data provided to update")
    #2-  je recupere le objet shipement de type Shipement model de ma dabe
    shipment = await session.get(Shipment,id)
    if shipment is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="given id dot not exists")
    #3- shipement de Type Shipment de model sql contien une methode sqlmodel_update pour mettre ajour l'objet
    shipment.sqlmodel_update(update_data)
    #4- je renvois l obejtnouveau vers ma data base
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment



# # #effacer un shipment
@router.delete('/shipment/{id}')
async def delete_shipment(id:int ,session:SessionDep)->dict[str,str]:
    shipment =  await session.get(Shipment,id)
 
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="shipment do not exsite the the given id")

    await session.delete(shipment)
    await session.commit()
    return {"id":"deleted success"}
