import app.routers.cities

validation_error_response = {"message": "Ошибка валидации"}

city_app_error_response = {"message": "Какая-то ошибка"}


def test_get_all_cities(client, create_city):
    response = client.get("/city/")
    assert response.status_code == 200
    assert response.json() == [create_city]


def test_asd(client, create_city, monkeypatch, session):
    response = client.get("/city/")

    def fake_get_cities(*args, **kwargs):
        raise Exception

    monkeypatch.setattr(app.routers.cities.cities_utils, "get_cities", fake_get_cities)
    assert response.status_code == 200
    assert response.json() == [create_city]


def test_get_all_cities_error(patch_client):
    response = patch_client.get("/city/")
    assert response.status_code == 400
    assert response.json() == city_app_error_response


def test_get_all_streets_by_city(client, create_city, create_street):
    response = client.get(f"/city/{create_city["id"]}/street")
    assert response.status_code == 200
    assert response.json() == [create_street]

    error_response = client.get(f"/city/qwe/street")
    assert error_response.status_code == 400
    assert error_response.json() == validation_error_response


def test_get_all_streets_by_city_error(patch_client):
    response = patch_client.get("/city/1/street")
    assert response.status_code == 400
    assert response.json() == city_app_error_response


def test_create_shop(client, create_city, create_street):
    response = client.post(
        "/shop/",
        json={
            "name": "string",
            "city_id": create_city["id"],
            "street_id": create_street["id"],
            "house": "test_house",
            "time_open": "14:27:04.808Z",
            "time_close": "14:27:04.808Z",
        },
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert type(response.json()["id"]) is int
    assert response.json()["id"] > 0

    response = client.post("/shop/", json={"name": "string"})
    assert response.status_code == 400
    assert response.json() == validation_error_response


def test_create_shop_error(patch_client):
    response = patch_client.post(
        "/shop/",
        json={
            "name": "string",
            "city_id": 1,
            "street_id": 1,
            "house": "test_house",
            "time_open": "14:27:04.808Z",
            "time_close": "14:27:04.808Z",
        },
    )
    assert response.status_code == 400
    assert response.json() == city_app_error_response


def test_get_shops(client, create_shop):
    response = client.get("/shop/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": create_shop["id"],
            "name": create_shop["name"],
            "city": create_shop["city"].name,
            "street": create_shop["street"].name,
            "house": create_shop["house"],
            "time_open": f"{create_shop["time_open"].hour}:{create_shop["time_open"].minute}:00Z",
            "time_close": f"{create_shop["time_close"].hour}:{create_shop["time_close"].minute}:00Z",
        }
    ]


def test_get_shops_error(patch_client):
    response = patch_client.get("/shop/")
    assert response.status_code == 400
    assert response.json() == city_app_error_response


def test_get_shops_with_street(client, create_shop):
    response = client.get("/shop/?street=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": create_shop["id"],
            "name": create_shop["name"],
            "city": create_shop["city"].name,
            "street": create_shop["street"].name,
            "house": create_shop["house"],
            "time_open": f"{create_shop["time_open"].hour}:{create_shop["time_open"].minute}:00Z",
            "time_close": f"{create_shop["time_close"].hour}:{create_shop["time_close"].minute}:00Z",
        }
    ]


def test_get_shops_with_city(client, create_shop):
    response = client.get("/shop/?city=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": create_shop["id"],
            "name": create_shop["name"],
            "city": create_shop["city"].name,
            "street": create_shop["street"].name,
            "house": create_shop["house"],
            "time_open": f"{create_shop["time_open"].hour}:{create_shop["time_open"].minute}:00Z",
            "time_close": f"{create_shop["time_close"].hour}:{create_shop["time_close"].minute}:00Z",
        }
    ]


def test_get_shops_with_open(client, create_shop, patch_open_time):
    response = client.get("/shop/?open=true")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": create_shop["id"],
            "name": create_shop["name"],
            "city": create_shop["city"].name,
            "street": create_shop["street"].name,
            "house": create_shop["house"],
            "time_open": f"{create_shop["time_open"].hour}:{create_shop["time_open"].minute}:00Z",
            "time_close": f"{create_shop["time_close"].hour}:{create_shop["time_close"].minute}:00Z",
        }
    ]


def test_get_shops_with_close(client, close_shop, patch_close_time):
    response = client.get("/shop/?open=false")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": close_shop["id"],
            "name": close_shop["name"],
            "city": close_shop["city"].name,
            "street": close_shop["street"].name,
            "house": close_shop["house"],
            "time_open": f"{close_shop["time_open"].hour}:{close_shop["time_open"].minute}:00Z",
            "time_close": f"{close_shop["time_close"].hour}:{close_shop["time_close"].minute}:00Z",
        }
    ]
