import json
import logging

from app import create_app

environment = "development"
app = create_app(environment)
client = app.test_client()

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

token = ""
product_id = None


def test_base_route():
    url = '/'
    response = client.get(url)
    assert response.status_code == 404


def test_login():
    global token
    url = '/auth'
    data = {
        "username": "erickdsama@gmail.com",
        "password": "123456"
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    response_json = response.json
    token = response_json.get("jwt", "")

    assert response.status_code == 200
    assert response.json


def test_post_product():
    global product_id
    url = '/products/'
    string_auth = 'Bearer {}'.format(token)
    headers['Authorization'] =  string_auth
    print(f'respo {string_auth}')

    data = {
        "title": "Computadora Asus",
        "brand": "Asus",
        "sku": "ASUS2302i25ss",
        "summary": "Laptop Asus i5, 4g RAM 500GB SSD",
        "photo": "no-photo",
        "long_description": "Laptop Asus 43430 con procesador intel i5 septima generacion"
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    product_id = response.json.get("id")
    assert response.status_code == 200


def test_get_products():
    url = '/products/'
    string_auth = 'Bearer {}'.format(token)
    headers['Authorization'] = string_auth
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_get_product():
    url = f'/product/{product_id}'
    string_auth = 'Bearer {}'.format(token)
    headers['Authorization'] = string_auth
    response = client.get(url, headers=headers)
    assert response.status_code == 200