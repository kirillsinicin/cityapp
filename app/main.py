from fastapi import FastAPI
from app.routers.cities import city_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(city_router)
