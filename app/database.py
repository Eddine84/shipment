from contextlib import contextmanager
import sqlite3
from typing import Any
from app.api.schemas.shipment import ShipementCreate,ShipementUpdate,ShipementRead



class DataBase:
    # def __init__(self) -> None:
    #     self.conn = sqlite3.connect('sqlite.db', check_same_thread=False)
    #     self.cur = self.conn.cursor()
    #     self.create_table("shipment")
    
    def connect_to_data_base(self):
        self.conn = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    
    def create_table(self,name):
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
               id INTEGER PRIMARY KEY,
                content TEXT, 
               weight REAL , 
               status TEXT,
               destination INTEGER
        ) """)
    #create
    def create(self,shipment:ShipementCreate)->int:
        self.cur.execute("""
        SELECT max(id) FROM shipment 
        """)
        id:int = self.cur.fetchone()[0]
        new_id:int = id+1
        self.cur.execute("""
        INSERT INTO shipment VALUES( :id, :content, :weight, :status, :destination )
        """,{
            "id":new_id,
            "status":"placed",
            **shipment.model_dump()
        })
        self.conn.commit()
        return new_id
    #read


    def get(self,id:int)->dict[str,Any] | None:
        self.cur.execute("""
         SELECT * FROM shipment WHERE id = ?
         """,(id,))

        shipment = self.cur.fetchone()
      
        return {
                "id":shipment[0],
                "content":shipment[1],
                "weight":shipment[2],
                "status":shipment[3],
                "destination":shipment[4],
            } if shipment else None
      

    #update
    def update(self,id:int,shipment:ShipementUpdate)->dict[str,Any] | None:
        self.cur.execute("""
                   UPDATE shipment SET status = :status
                   WHERE id = :id
    """,{
        "id":id ,
        **shipment.model_dump()
        })
        self.conn.commit()
        return self.get(id)
    
    #delete
    def delete(self,id:int)->None:
        self.cur.execute(""" DELETE FROM shipment WHERE id = ?""",(id,))
        self.conn.commit()
        return None
    


    def get_latest(self)->dict[Any,str] | None:
        self.cur.execute("""
        SELECT * FROM shipment ORDER BY id DESC LIMIT 1
        """)
        row = self.cur.fetchone()
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3],
            "destination":row[4]
        }if row is not None else None
    
    def close(self):
        self.conn.close()


@contextmanager
def managed_db():
    print("connected to db")
    db = DataBase()
    db.connect_to_data_base()
    db.create_table("shipment")
    yield db
    print("connection to db closed")
    db.close()



with managed_db() as db:
    db.get(1)


