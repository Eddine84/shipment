from sqlalchemy import create_engine
from sqlmodel import SQLModel,Session
from typing import Annotated
from fastapi import Depends

#1- creation engine
engine = create_engine(url='sqlite:///sqlite.db',
              echo=True,#pour affiche le resultat dans terminal
              connect_args={ 
                  "check_same_thread":False }
              )
from .models import Shipment

# creation table et equipement engine et exportation vers life span pour demarer au debut du serveur
def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep =  Annotated[Session,Depends(get_session)]




# * **L’engine = le robot physique** (la machine prête à agir, par exemple une tronçonneuse, mais sans commandes il ne fait rien)
# * **La metadata = le logiciel avec ses instructions** (boutons « couper », « arrêter », « couper lentement »…)
# * **`SQLModel.metadata.create_all(bind=engine)` = installer ce logiciel dans le robot**
#   → Ça permet au robot (engine) de savoir comment manipuler la base de données : créer les tables, gérer les colonnes, etc.

# Sans ce logiciel (metadata), même si tu as la tronçonneuse (engine), tu ne peux rien faire avec car tu ne peux pas lui dire quoi faire.

# Une fois la metadata installée dans l’engine, tu peux lui envoyer des instructions (requêtes SQL via Python) et le robot sait comment agir.


