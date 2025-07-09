

from fastapi import FastAPI,HTTPException,status
from app.schemas import ShipementRead,ShipementCreate,ShipementUpdate, ShipmentStatus
from app.database.session import create_db_tables,SessionDep
from app.database.models import Shipment
from contextlib import asynccontextmanager
from rich import print, panel
from datetime import datetime, timedelta



@asynccontextmanager
async def life_span_handler(app:FastAPI):
    print(panel.Panel("server started", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("server closed",border_style="red"))



app = FastAPI(lifespan=life_span_handler)



# #recuperer le dernier shipement de list
# @app.get('/shipment/latest',response_model=ShipementRead)
# async def get_latest_shipment(session:SessionDep):
#     stmt = select(Shipment).order_by(Shipment.id.desc()).limit(1) # type: ignore
#     result = await session.exec(stmt)
#     shipment = result.scalars().first()
#     #last_shipment=  db.get_latest() 
#     if shipment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not shipment found")
#     return shipment





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
# @app.get('/shipment/field/{field}', response_model=ShipementRead)
# async def get_shipment_field(id:int,field:str ,session:SessionDep)->dict[str,Any]:

#     shipment = db.get(id)
#     if shipment is None:
#         raise HTTPException(
#             detail="Given id doesn't exist!!",
#             status_code=status.HTTP_404_NOT_FOUND
#         )
    
#     if field not in shipment:
#         raise HTTPException(
#             detail="Given key doesn't exist!!",
#             status_code=status.HTTP_404_NOT_FOUND
#         )
#     return shipment[field]


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
# @app.delete('/shipment/{id}')
# async def delete_shipment(id:int)->dict[str,Any]:
#     shipment = db.get(id)
#     if shipment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="shipment do not exsite the the given id")
#     db.delete(id)
#     return {"id":id,"msg":"deleted success"}
