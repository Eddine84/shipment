import sqlite3
from typing import Any
from .schemas import ShipementCreate,ShipementUpdate,ShipementRead



class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table("shipment")
    
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
    


    def get_latest(self)->ShipementRead:
        self.cur.execute("""
        SELECT * FROM shipment ORDER BY id DESC LIMIT 1
        """)
        result = self.cur.fetchone()
        return ShipementRead(
            id=result[0],
            content=result[1],
            weight=result[2],
            status=result[3],
            destination=result[4]
        )
    
    def close(self):
        self.conn.close()





db = DataBase()
db.get(12703)


# creer la ressrouce vers fichier creer sqlite.db
# connection = sqlite3.connect('sqlite.db')



# cursor = connection.cursor()

# 1. Create a Table
# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS shipment (
#                id INTEGER PRIMARY KEY,
#                 content TEXT, 
#                weight REAL , 
#                status TEXT,
#                destination INTEGER
#         ) """)

# 1Bis. Delete all Table
# cursor.execute('DROP TABLE shipment')
# connection.commit()


#2. Insert Shipment Data
# cursor.execute(""" 
#             INSERT INTO shipment 
#             VALUES (12706, 'chair', 4, 'out_of_delevery', 1200 )
#         """)

# connection.commit()

# 3. Read a Shipment by id
# cursor.execute(""" SELECT * FROM shipment WHERE weight = 30 """)
# data = cursor.fetchone() #pour chercher la premier
# data = cursor.fetchall() #pour chercher tout
# print(data)


# id= 12703
# status = "placed"

# # 4. Update A Shipment by id
# cursor.execute("""
#                UPDATE shipment SET status = :status
#                WHERE id > :id
# """,{"status":status,"id":id})   
# connection.commit()     



# 5. Delete a Shipment by id
# cursor.execute(""" DELETE FROM shipment WHERE id = 12703""")
# connection.commit()

#une fois fini je cloture ma connection vers db
# connection.close()














# 1. sqlite3.connect('sqlite.db')
# Cette fonction ouvre une connexion à ta base de données SQLite.

# Si le fichier 'sqlite.db' n'existe pas sur le disque, SQLite va le créer.

# La connexion représente un objet en mémoire qui sert à dialoguer avec la base.

# Cette connexion gère la communication, transactions, verrous, etc.


# 2. connection.cursor()
# C'est une méthode appelée sur la connexion.

# Elle crée un curseur (cursor) qui est un objet permettant d’exécuter des commandes SQL (requêtes, insertions, updates, etc.).

# Le curseur sert d’interface pour envoyer des instructions SQL vers la base et récupérer les résultats.

# En gros, c’est comme un « outil de requêtage » lié à ta connexion.


# Analogie simple :
# La connexion est comme un téléphone entre toi (ton programme) et la base.

# Le curseur est comme la ligne sur laquelle tu passes des appels précis (requêtes).

# Tu peux avoir plusieurs curseurs (lignes) sur la même connexion (téléphone).

# Pourquoi on utilise un curseur ?
# Parce que tu peux exécuter plusieurs requêtes, et le curseur garde la trace du résultat de la dernière.

# Il permet de parcourir les résultats ligne par ligne (fetchone, fetchall).

# Le curseur est léger et temporaire, tu peux en créer plusieurs si besoin.



# from typing import Any
# import json


# shipments:dict[int,Any] = {


# }



# with open('./shipment.json' ) as json_file:
#    data = json.load(json_file)
#    for shipment in data:
#       shipments[shipment["id"]] = shipment





# def save():
#    with open('./shipment.json', "w") as json_file_update:
#       json.dump(list( shipments.values()),json_file_update, indent=2)
      
