
from fastapi import FastAPI,HTTPException,status
from typing import Any
from .schemas import ShipementRead,ShipmentStatus,ShipementCreate,ShipementUpdate

app = FastAPI()

#recuperer le dernier shipement de list
@app.get('/shipment/latest')
async def get_latest_shipment()->dict[str,Any]:
    id:int = max(shipments.keys()) 
    return shipments[id]





# recuperer le shipement selon id 
@app.get('/shipment/{id}',response_model=ShipementRead)
async def get_shipment(id:int):
    if id not in shipments:
       raise HTTPException(
        detail="Given id doesn't exist!",
        status_code=status.HTTP_404_NOT_FOUND
       )
    shipment =  shipments[id]
    return shipment



#ajouter un nouveau shipment attention status est founi par defaut donc j ajoute pas a mon Shipment schema
@app.post('/shipment')
async def submit_shipment( shipment:ShipementCreate)->dict[str,int]:

    id:int = max(shipments.keys())+1
    new_shipment:dict[str,Any]= {
        "id":id,
        "weight":shipment.weight,
        "content":shipment.content,
        "status":"placed"

    }
    shipments[id] = new_shipment

    return {"id":id}



#recupéré la valeur d'une clés shipment
@app.get('/shipment/field/{field}')
async def get_shipment_field(id:int,field:str)->Any:
    if id not in shipments:
        raise HTTPException(
            detail="Given id doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
   
    if field not in shipments[id]:
        raise HTTPException(
            detail="Given key doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return shipments[id][field]


#metre ajour un shipment et ajouter Enum pour verifier valeur de field




@app.patch('/shipment/{id}', response_model=ShipementRead)
async def patch_shipment(id:int,shipment:ShipementUpdate):
    if id not in shipments:
        raise HTTPException(
            detail="Given key doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    shipments[id].update(shipment)
    return shipments[id]

#effacer un shipment
@app.delete('/shipment/{id}')
async def delete_shipment(id:int)->dict[str,Any]:
    if id not in shipments:
         raise HTTPException(
            detail="Given key doesn't exist!!",
            status_code=status.HTTP_404_NOT_FOUND
        )
    del shipments[id]
    return {"id":id,"msg":"deleted success"}

#liste des shipments    
shipments = {
    12701: {
        "weight": .6,
        "content": "glassware",
        "status":  "placed",
        "destination":1
    },
    12702: {
        "weight": 2.3,
        "content": "books",
        "status": "shipped", "destination":2
    },
    12703: {
        "weight": 1.1,
        "content": "electronics",
        "status": "delivered", "destination":1123123
    },
    12704: {
        "weight": 3.5,
        "content": "furniture",
        "status": "in transit", "destination":213123
    },
    12705: {
        "weight": .9,
        "content": "clothing",
        "status": "returned", "destination":110312
    },
    12706: {
        "weight": 4.0,
        "content": "appliances",
        "status": "processing", "destination":1412313
    },
    12707: {
        "weight": 1.8,
        "content": "toys",
        "status": "placed", "destination":10241333
    },
}


