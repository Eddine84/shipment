from datetime import datetime
from pydantic import BaseModel,Field
from app.database.models import ShipmentStatus








class ShipementBase(BaseModel):
    weight:float = Field(le=25, gt=0 , description="Maximum weight limit")
    content:str = Field(max_length=40,min_length=5 ,description="shipment content")
    destination:int  = Field( description="shipment destination details")



class ShipementRead(ShipementBase,BaseModel):
    id:int
    status:ShipmentStatus =Field(description="statut du signalement")
    estimated_delivery: datetime 




class ShipementCreate(ShipementBase,BaseModel):
        pass



class ShipementUpdate(BaseModel):
        status:ShipmentStatus | None =Field(default=None,description="statut du signalement")
        weight:float | None = Field(default=None)
        content:str | None = Field(default=None)
        destination:int | None  = Field(default=None)
        estimated_delivery: datetime | None = Field(default=None)

#= Field(default_factory=lambda: datetime.now() + timedelta(days=3))