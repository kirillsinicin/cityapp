from fastapi import APIRouter, Body, Depends, Query, HTTPException
from typing import Annotated, Sequence
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils import cities_utils
from app.schema import GetAllCitiesResponse, GetAllStreetsByCityResponse, CreateShopResponse, CreateShopRequest, \
    GetShopsResponse
import datetime

city_router = APIRouter()

task_exception = HTTPException(status_code=400, detail="400 для всех эндпоинтов")


@city_router.get("/city/")
def get_all_cities(db: Session = Depends(get_db)) -> list[GetAllCitiesResponse]:
    try:
        cities = cities_utils.get_cities(db)
    except Exception:
        raise task_exception
    return cities


@city_router.get("/city/{city_id}/street")
def get_all_streets_by_city(city_id: int, db: Session = Depends(get_db)) -> list[GetAllStreetsByCityResponse]:
    if type(city_id) is not int:
        raise task_exception
    city_streets = cities_utils.get_streets_by_city(db, city_id=city_id)
    return city_streets


@city_router.post("/shop/")
def create_shop(shop: Annotated[CreateShopRequest, Body()], db: Session = Depends(get_db)) -> CreateShopResponse:
    shop = cities_utils.create_shop(db, shop=shop)
    return CreateShopResponse(id=shop.id)


@city_router.get("/shop/")
def get_shops(
        db: Session = Depends(get_db),
        street_id: Annotated[int | None, Query(alias="street")] = None,
        city_id: Annotated[int | None, Query(alias="city")] = None,
        is_open: Annotated[bool, Query(alias="open")] = None
) -> Sequence[GetShopsResponse]:
    models = cities_utils.get_shops_by_filter(db, street_id, city_id, is_open)
    return [GetShopsResponse(
        id=model.id,
        name=model.name,
        city=model.street.city.name,
        street=model.street.name,
        house=model.house,
        time_open=datetime.time(model.time_open.hour, model.time_open.minute, tzinfo=datetime.UTC),
        time_close=datetime.time(model.time_close.hour, model.time_close.minute, tzinfo=datetime.UTC)
    ) for model in models]
