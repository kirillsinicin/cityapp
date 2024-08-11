from fastapi import FastAPI
from app.routers.cities import city_router

app = FastAPI()

app.include_router(city_router)
