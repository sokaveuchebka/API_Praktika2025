from fastapi import FastAPI
from database import Base, engine
from auth import router as auth_router
from items import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(items_router, prefix="/items", tags=["Items"])
