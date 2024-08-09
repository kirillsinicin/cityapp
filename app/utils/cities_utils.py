from typing import Sequence

from sqlalchemy.orm import Session
from app.schema import CreateShopRequest
from app import models
from sqlalchemy import select
from datetime import datetime, UTC


def get_cities(db: Session):
    return db.scalars(select(models.City)).all()


def get_streets_by_city(db: Session, city_id: int):
    return db.scalars(select(models.Street).where(models.Street.city_id == city_id)).all()


def create_shop(db: Session, shop: CreateShopRequest):
    db_shop = models.Shop(name=shop.name, street_id=shop.street_id, house=shop.house,
                          time_open=shop.time_open,
                          time_close=shop.time_close)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def get_shops_by_filter(db: Session, street_id: int | None = None, city_id: int | None = None,
                        is_open: bool | None = None) -> Sequence[models.Shop]:
    base_stmt = select(models.Shop)
    current_time = datetime.now(UTC).time()
    if street_id is not None:
        base_stmt = base_stmt.where(models.Shop.street_id == street_id)
    if city_id is not None:
        base_stmt = base_stmt.join(models.Shop.street).where(models.Street.city_id == city_id)
    if is_open is True:
        base_stmt = base_stmt.where(models.Shop.time_open <= current_time).where(
            current_time < models.Shop.time_close)
    if is_open is False:
        base_stmt = base_stmt.where(models.Shop.time_open < current_time).where(
            models.Shop.time_close < current_time)
    return db.scalars(base_stmt).all()
