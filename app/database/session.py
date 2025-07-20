from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

import app.database.models

##1- creation engine  asyncsynchrone  (object pre a lemplois pour creer une connection physique, lire ecrire a travers des session mais pas encore branché ni en etat de marche)

engine = create_async_engine(url=settings.POSTGRES_URL, echo=True)


async def create_db_tables():
    # creaition vrais ressouce matereil enrre ram et db grace a aenter() et cloture cette conenction avec aexit()
    async with engine.begin() as connection:
        # je met directement la fonction SQLModel.metadata.create_all() pour la rendre async car asyncio va la mettre  dans un thread separer pour lexecuter si non elle va etre syncrhnet blocante et je pert linteret de l 'asynchnosme
        await connection.run_sync(SQLModel.metadata.create_all)


# get_session est une fonction asynchrone génératrice utilisée pour la DI de FastAPI.
async def get_session():
    # 1️⃣ Création d’une usine de sessions asynchrones liée à l’engine.
    #    Attention : ici, on configure seulement — aucune connexion n’est encore ouverte.
    Async_Session = sessionmaker(
        bind=engine,  # engine = objet async prêt à établir des connexions # type: ignore
        class_=AsyncSession,  # indique qu’on veut une session async
        expire_on_commit=False,
    )  # type: ignore

    # 2️⃣ Ouverture d’une session via async context manager :
    #    Cela déclenche :
    #    - l’ouverture d’une connexion réelle à la DB via `engine` (dans __aenter__)
    #    - la création d’un objet `session` lié à cette connexion
    async with Async_Session() as session:  # type: ignore
        # 3️⃣ FastAPI reçoit la session via `yield` pour exécuter la route.
        yield session

    # 4️⃣ Une fois la route terminée :
    #    - __aexit__ est appelé automatiquement
    #    - Cela ferme proprement la session
    #    - Et ferme la connexion réelle à la base de données via l'engine


# SessionDep = Annotated[AsyncSession,Depends(get_session)]
