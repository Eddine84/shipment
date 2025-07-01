from pydantic import BaseModel,Field
from enum import Enum

class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"






class ShipementBase(BaseModel):
    weight:float = Field(le=25, gt=0 , description="Maximum weight limit")
    content:str = Field(max_length=40,min_length=5 ,description="shipment content")
    destination:int  = Field( description="shipment destination details")



class ShipementRead(ShipementBase,BaseModel):
    status:ShipmentStatus =Field(description="statut du signalement")


# class Order(BaseModel):
#     price:int
#     title:str
#     description:str


class ShipementCreate(ShipementBase,BaseModel):
    pass



class ShipementUpdate(BaseModel):
        status:ShipmentStatus =Field(description="statut du signalement")
        weight:float | None = Field(default=None, description="Maximum weight limit")
        content:str | None = Field(default=None, description="shipment content")
        destination:int | None  = Field(default=None,  description="shipment destination details")
