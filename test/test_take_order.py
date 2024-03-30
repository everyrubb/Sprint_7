import allure
import requests
from const import Const, MessageText


class TestTakeOrder:

    @allure.title('Успешное принятие заказа')
    def test_take_order(self, take_id_order, create_courier):
        id_order = take_id_order
        id_courier = create_courier
        response_take_order = requests.put(f'{Const.TAKE_ORDER}{id_order}?courierId={id_courier}')
        assert response_take_order.status_code == 200
        assert MessageText.TAKE_ORDER in response_take_order.text

    @allure.title('Принятие заказа без id заказа')
    def test_take_order_without_id_order(self, create_courier):
        id_courier = create_courier
        response_take_order = requests.put(f'{Const.TAKE_ORDER}?courierId={id_courier}')
        # Баг на бэке. Присылается 'code:404,message:Not Found'
        assert response_take_order.status_code == 400
        assert MessageText.TAKE_ORDER_WITHOUT_ID_COURIER_ORDER in response_take_order.text

    @allure.title('Принятие заказа без id курьера')
    def test_take_order_without_id_courier(self, take_id_order):
        id_order = take_id_order
        response_take_order = requests.put(f'{Const.TAKE_ORDER}{id_order}')
        assert response_take_order.status_code == 400
        assert MessageText.TAKE_ORDER_WITHOUT_ID_COURIER_ORDER in response_take_order.text

    @allure.title('Принятие заказа с несуществующим id заказа')
    def test_take_order_fake_id_order(self, take_id_order, create_courier):
        id_order = take_id_order
        id_courier = create_courier
        response_take_order = requests.put(f'{Const.TAKE_ORDER}{id_order}1?courierId={id_courier}')
        assert response_take_order.status_code == 404
        assert MessageText.TAKE_ORDER_FAKE_ID in response_take_order.text

    @allure.title('Принятие заказа с несуществующим id курьера')
    def test_take_order_fake_id_courier(self, take_id_order, create_courier):
        id_order = take_id_order
        id_courier = create_courier
        response_take_order = requests.put(f'{Const.TAKE_ORDER}{id_order}?courierId={id_courier}32')
        assert response_take_order.status_code == 404
        assert MessageText.TAKE_ORDER_FAKE_ID_COURIER in response_take_order.text

    @allure.title('Принятие заказа дважды')
    def test_take_order_twice(self, take_id_order, create_courier):
        id_order = take_id_order
        id_courier = create_courier
        requests.put(f'{Const.TAKE_ORDER}{id_order}?courierId={id_courier}')
        response_take_order_twice = requests.put(f'{Const.TAKE_ORDER}{id_order}?courierId={id_courier}')
        assert response_take_order_twice.status_code == 409
        assert MessageText.TAKE_ORDER_FAKE_TWICE in response_take_order_twice.text
