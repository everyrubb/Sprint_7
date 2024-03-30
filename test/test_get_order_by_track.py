import allure
import requests
from const import MessageText, Const


class TestGetOrderByTrack:

    @allure.title('Проверка получения заказа по его номеру')
    def test_get_order_by_track(self, create_order):
        track = create_order
        response_get_id_order = requests.get(f'{Const.GET_ORDER_TRACK}?t={track}')
        assert response_get_id_order.status_code == 200
        assert MessageText.GET_ORDER in response_get_id_order.text

    @allure.title('Проверка получения заказа без номера')
    def test_get_order_by_track(self):
        response_get_id_order = requests.get(f'{Const.GET_ORDER_TRACK}?t=')
        assert response_get_id_order.status_code == 400
        assert MessageText.GET_ORDER_WITHOUT_TRACK in response_get_id_order.text

    @allure.title('Проверка получения заказа без номера')
    def test_get_order_by_track(self):
        response_get_id_order = requests.get(f'{Const.GET_ORDER_TRACK}?t=02930202')
        assert response_get_id_order.status_code == 404
        assert MessageText.GET_ORDER_FAKE_TRACK in response_get_id_order.text
