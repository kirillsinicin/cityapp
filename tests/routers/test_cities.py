def test_get_all_cities(client, create_city):
    response = client.get("/city/")
    assert response.status_code == 200
    assert response.json() == [create_city]


def test_get_all_streets_by_city(client, create_city, create_street):
    response = client.get(f"/city/{create_city["id"]}/street")
    assert response.status_code == 200
    assert response.json() == [create_street]


def test_create_shop(client, create_city, create_street):
    response = client.post("/shop/", json={"name": "string",
                                           "city_id": create_city["id"],
                                           "street_id": create_street["id"],
                                           "house": "test_house",
                                           "time_open": "14:27:04.808Z",
                                           "time_close": "14:27:04.808Z"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert type(response.json()["id"]) is int
    assert response.json()["id"] > 0


# def test_get_shops(client, create_shop):
#     response = client.get("/shop/")
#     assert response.status_code == 200
#     assert response.json() == [{
#         "id": create_shop["id"],
#         "name": create_shop["name"],
#         "city": create_shop["city"].name,
#         "street": create_shop["street"].name,
#         "house": create_shop["house"],
#         "time_open": create_shop["time_open"].strftime("%Z"),
#         "time_close": create_shop["time_close"]
#     }]
#
#
# def test_get_shops_with_street():
#     response = client.get("/shop/?street=2")
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# def test_get_shops_with_city():
#     response = client.get("/shop/?city=2")
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# def test_get_shops_with_open():
#     response = client.get("/shop/?open=false")
#     assert response.status_code == 200
#     assert response.json() == data_to_get_shops_where_open_false
