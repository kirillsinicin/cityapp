from datetime import time
from pydantic import BaseModel


class GetAllCitiesResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GetAllStreetsByCityResponse(BaseModel):
    id: int
    name: str
    city_id: int

    class Config:
        from_attributes = True


class CreateShopRequest(BaseModel):
    name: str
    city_id: int
    street_id: int
    house: str
    time_open: time
    time_close: time


class CreateShopResponse(BaseModel):
    id: int


class GetShopsResponse(BaseModel):
    id: int
    name: str
    city: str
    street: str
    house: str
    time_open: time
    time_close: time

    class Config:
        from_attributes = True
