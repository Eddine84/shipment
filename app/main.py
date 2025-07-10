

from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from sqlmodel import select


from fastapi import FastAPI, HTTPException, status
from rich import panel, print

from app.database.models import Shipment
from app.database.session import SessionDep, create_db_tables
from app.schemas import ShipementCreate, ShipementRead, ShipementUpdate, ShipmentStatus


@asynccontextmanager
async def life_span_handler(app:FastAPI):
    print(panel.Panel("server started", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("server closed",border_style="red"))



app = FastAPI(lifespan=life_span_handler)



# #recuperer le dernier shipement de list
@app.get('/shipment/latest',response_model=ShipementRead)
async def get_latest_shipment(session:SessionDep):
    stmt = select(Shipment).order_by(Shipment.id.desc()) # type: ignore
    result =  session.exec(stmt).first()
    if result is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not shipment found")
    return result





# # recuperer le shipement selon id 
@app.get('/shipment/{id}',response_model=ShipementRead)
async def get_shipment(id:int , session:SessionDep):
    shipment = session.get(Shipment,id)
    if shipment is None:
       raise HTTPException(
        detail="Given id doesn't exist!",
        status_code=status.HTTP_404_NOT_FOUND
       )
    

    return shipment



# #ajouter un nouveau shipment attention status est founi par defaut donc j ajoute pas a mon Shipment schema
@app.post('/shipment',response_model=None)
async def submit_shipment( shipment:ShipementCreate, session:SessionDep)->dict[str,int]:

    shipment_to_senf =  Shipment(**shipment.model_dump(),status=ShipmentStatus.placed, estimated_delivery=datetime.now() + timedelta(days=3))
    session.add(shipment_to_senf)
    session.commit()
    session.refresh(shipment_to_senf)
    return {"id":shipment_to_senf.id}
    



# #recupéré la valeur d'une clés shipment
@app.get('/shipment/field/{field}', response_model=dict)
async def get_shipment_field(id: int, field: str, session: SessionDep) -> dict[str, any]:
    stmt = select(Shipment).where(Shipment.id == id)
    shipment = session.exec(stmt).first()

    if shipment is None:
        raise HTTPException(404, "Shipment not found")


    if not hasattr(shipment, field):
        raise HTTPException(404, "Field not in Shipment")

    return {field: getattr(shipment, field)}




#front envoyer shipment update mais il ya quelqu valeur None, donc leve pas l'erruer
#erreur peut etre levé dans la conversion en dictionnaire vers la databse car il sont requi , donc je dois assureé excluede none pour ne pas assigner none et mettre ajouer que les chamos fourni


@app.patch('/shipment/{id}', response_model=ShipementRead )
async def update_shipment(id:int,shipment_update:ShipementUpdate , session:SessionDep) :

    #1 - je converti mon objet schema Basemodel en dictionnaire et retir les valeur non fourni
    update_data = shipment_update.model_dump(exclude_none=True)
    if update_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no data provided to update")
    #2-  je recupere le objet shipement de type Shipement model de ma dabe
    shipment =session.get(Shipment,id)
    if shipment is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="given id dot not exists")
    #3- shipement de Type Shipment de model sql contien une methode sqlmodel_update pour mettre ajour l'objet
    shipment.sqlmodel_update(update_data)
    #4- je renvois l obejtnouveau vers ma data base
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment



# #effacer un shipment
@app.delete('/shipment/{id}')
async def delete_shipment(id:int ,session:SessionDep)->dict[str,str]:
    shipment =  session.get(Shipment,id)
 
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="shipment do not exsite the the given id")

    session.delete(shipment)
    session.commit()
    return {"id":"deleted success"}



