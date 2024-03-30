import pytest
import requests

from const import Const, MessageText
from helpers import Helpers


@pytest.fixture(scope='function')
def helpers():
    return Helpers()

@pytest.fixture(scope='function')
def create_order():
    person_data = [
        ['Naruto', 'Uchiha', 'Konoha, 192 apt.', '4', '+7 800 355 35 35', '5', '2020-06-06','Saske, come back to Konoha', "BLACK"]
    ]
    response_create_order = requests.post(Const.CREATE_ORDER, json=person_data)
    track = response_create_order.json()['track']
    assert response_create_order.status_code == 201 and MessageText.CREATE_ORDER in response_create_order.text
    return track

@pytest.fixture(scope='function')
def take_id_order(create_order):
    track = create_order
    response_get_id_order = requests.get(f'{Const.GET_ORDER_TRACK}?t={track}')
    id_order = response_get_id_order.json()['order']['id']
    assert response_get_id_order.status_code == 200 and MessageText.GET_ORDER in response_get_id_order.text
    return id_order

@pytest.fixture(scope='function')
def create_courier(helpers):
    data = helpers.register_new_courier_and_return_login_password()
    response_post = requests.post(Const.LOGIN_COURIER, data={
        "login": data[0],
        "password": data[1],
    })
    assert response_post.status_code == 200 and MessageText.LOGING_COURIER in response_post.text
    courier_id = response_post.json()['id']
    yield courier_id
    requests.delete(f'{Const.DELETE_COURIER}/{courier_id}')
