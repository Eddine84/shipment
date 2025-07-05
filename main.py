
from fastapi import FastAPI,HTTPException,status
from typing import Any
from .schemas import ShipementRead,ShipementCreate,ShipementUpdate
from .database import DataBase

app = FastAPI()
db = DataBase()



#recuperer le dernier shipement de list
@app.get('/shipment/latest',response_model=ShipementRead)
async def get_latest_shipment()->ShipementRead:
    last_shipment:ShipementRead=  db.get_latest() 
    return last_shipment





# recuperer le shipement selon id 
@app.get('/shipment/{id}',response_model=ShipementRead)
async def get_shipment(id:int):
    shipment =  db.get(id)
    if shipment is None:
       raise HTTPException(
        detail="Given id doesn't exist!",
        status_code=status.HTTP_404_NOT_FOUND
       )

    return shipment



#ajouter un nouveau shipment attention status est founi par defaut donc j ajoute pas a mon Shipment schema
@app.post('/shipment',response_model=None)
async def submit_shipment( shipment:ShipementCreate)->dict[str,int]:
    shipment_id:int = db.create(shipment)
    return {"id":shipment_id}



#recupéré la valeur d'une clés shipment
@app.get('/shipment/field/{field}')
async def get_shipment_field(id:int,field:str)->Any:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            detail="Given id doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if field not in shipment:
        raise HTTPException(
            detail="Given key doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return shipment[field]
# je decompose en deux get id -> retounr une shipment
# je get field je crer une methode dans la class 


#metre ajour un shipment et ajouter Enum pour verifier valeur de field




@app.patch('/shipment/{id}', response_model=ShipementRead )
async def update_shipment(id:int,shipment:ShipementUpdate) ->dict[str,Any]| None:
    updated_shipment = db.update(id,shipment)
    if updated_shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="given id dot not exists")
    return updated_shipment



#effacer un shipment
@app.delete('/shipment/{id}')
async def delete_shipment(id:int)->dict[str,Any]:
    db.delete(id)
    return {"id":id,"msg":"deleted success"}
