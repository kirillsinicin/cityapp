import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app import models
from app.db import get_db
import pytest

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://kiruha:kiruha@localhost:8987/kiruha"
fake_open_time = datetime.time(14, tzinfo=datetime.timezone.utc)
fake_close_time = datetime.time(22, tzinfo=datetime.timezone.utc)


@pytest.fixture
def engine():
    return create_engine(
        SQLALCHEMY_DATABASE_URL
    )


@pytest.fixture
def session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield TestingSessionLocal()


@pytest.fixture
def create_city(session):
    city = models.City(name="Saratov2")
    session.add(city)
    session.commit()
    session.refresh(city)
    return {
        "id": city.id,
        "name": city.name
    }


@pytest.fixture
def create_street(session, create_city):
    street = models.Street(name="Рудченко2", city_id=create_city["id"])
    session.add(street)
    session.commit()
    session.refresh(street)
    return {
        "id": street.id,
        "name": street.name,
        "city_id": street.city_id,
    }


@pytest.fixture
def create_shop(session, create_city, create_street):
    shop = models.Shop(
        name="string",
        street_id=create_street["id"],
        house="test_house",
        # time_open="9:00:00.808Z",
        time_open=datetime.time(10, 10, tzinfo=datetime.timezone.utc),
        # time_close="21:00:00.808Z"
        time_close=datetime.time(21, 21, tzinfo=datetime.timezone.utc)
    )
    session.add(shop)
    session.commit()
    session.refresh(shop)
    return {
        "id": shop.id,
        "name": shop.name,
        "city": shop.street.city,
        "street": shop.street,
        "house": shop.house,
        "time_open": shop.time_open,
        "time_close": shop.time_close
    }


@pytest.fixture
def close_shop(session, create_city, create_street):
    shop = models.Shop(
        name="string",
        street_id=create_street["id"],
        house="test_house",
        # time_open="9:00:00.808Z",
        time_open=datetime.time(11, 10, tzinfo=datetime.timezone.utc),
        # time_close="21:00:00.808Z"
        time_close=datetime.time(11, 11, tzinfo=datetime.timezone.utc)
    )
    session.add(shop)
    session.commit()
    session.refresh(shop)
    return {
        "id": shop.id,
        "name": shop.name,
        "city": shop.street.city,
        "street": shop.street,
        "house": shop.house,
        "time_open": shop.time_open,
        "time_close": shop.time_close
    }


@pytest.fixture
def client(engine, session):
    from app.main import app

    models.Base.metadata.create_all(bind=engine)

    def get_test_db():
        db = session
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client

    models.Base.metadata.drop_all(engine)


@pytest.fixture
def patch_open_time(monkeypatch):
    class OpenTime(datetime.datetime):
        @classmethod
        def now(cls):
            return fake_open_time

    monkeypatch.setattr(datetime, 'datetime', fake_open_time)


@pytest.fixture
def patch_close_time(monkeypatch):
    class CloseTime(datetime.datetime):
        @classmethod
        def now(cls):
            return fake_close_time

    monkeypatch.setattr(datetime, 'datetime', fake_close_time)
