import datetime
from typing import Annotated, Sequence

from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.schema import (
    CreateShopRequest,
    CreateShopResponse,
    GetAllCitiesResponse,
    GetAllStreetsByCityResponse,
    GetShopsResponse,
)
from app.utils import cities_utils

city_router = APIRouter()


class CityAppException(Exception):
    response = JSONResponse(
        status_code=400,
        content={"message": "Какая-то ошибка"},
    )


@city_router.get("/city/")
def get_all_cities(db: Session = Depends(get_db)) -> list[GetAllCitiesResponse]:
    try:
        cities = cities_utils.get_cities(db)
    except Exception as e:
        raise CityAppException from e
    return cities


@city_router.get("/city/{city_id}/street")
def get_all_streets_by_city(
    city_id: int, db: Session = Depends(get_db)
) -> list[GetAllStreetsByCityResponse]:
    try:
        city_streets = cities_utils.get_streets_by_city(db, city_id=city_id)
    except Exception as e:
        raise CityAppException from e
    return city_streets


@city_router.post("/shop/")
def create_shop(
    shop: Annotated[CreateShopRequest, Body()], db: Session = Depends(get_db)
) -> CreateShopResponse:
    try:
        shop = cities_utils.create_shop(db, shop=shop)
    except Exception as e:
        raise CityAppException from e
    return CreateShopResponse(id=shop.id)


@city_router.get("/shop/")
def get_shops(
    db: Session = Depends(get_db),
    street_id: Annotated[int | None, Query(alias="street")] = None,
    city_id: Annotated[int | None, Query(alias="city")] = None,
    is_open: Annotated[bool, Query(alias="open")] = None,
) -> Sequence[GetShopsResponse]:
    try:
        models = cities_utils.get_shops_by_filter(db, street_id, city_id, is_open)
    except Exception as e:
        raise CityAppException from e
    return [
        GetShopsResponse(
            id=model.id,
            name=model.name,
            city=model.street.city.name,
            street=model.street.name,
            house=model.house,
            time_open=datetime.time(
                model.time_open.hour, model.time_open.minute, tzinfo=datetime.UTC
            ),
            time_close=datetime.time(
                model.time_close.hour, model.time_close.minute, tzinfo=datetime.UTC
            ),
        )
        for model in models
    ]
