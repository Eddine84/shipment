from datetime import datetime
from sqlmodel import SQLModel,Field
from enum import Enum



class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

#id pas fourni dans la requuete sql table va le creer et incrementer
    id:int  = Field( default=None,primary_key=True)
    content:str 
    weight:float =Field(le=25, gt=0 , description="Maximum weight limit")
    destination:int
    status:ShipmentStatus
    estimated_delivery:datetime