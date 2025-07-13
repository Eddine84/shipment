
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel, print

from app.api.router import router
from app.database.session import create_db_tables


@asynccontextmanager
async def life_span_handler(app:FastAPI):
    print(panel.Panel("server started", border_style="green"))
    await create_db_tables()
    yield
    print(panel.Panel("server closed",border_style="red"))



app = FastAPI(lifespan=life_span_handler)













    
















app.include_router(router)

