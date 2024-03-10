import json

import allure
import pytest
import requests

from data import Orders
from urls import URLS


class TestCreateOrder:
    API_URL = f'{URLS.MAIN_URL}{URLS.CREATE_ORDER}'

    @pytest.mark.parametrize('data',
                             [{"color": ["BLACK"]},
                              {"color": ["GREY"]},
                              {"color": [""]},
                              {"color": ["BLACK", "GREY"]}
                              ])
    @allure.title('Проверка на создание заказа')
    def test_create_order(self, data):
        order_data = json.dumps(Orders.data_order.update(data))
        response = requests.post(self.API_URL, data=order_data)
        assert response.status_code == 201 and 'track' in response.text


class TestOrderList:
    API_URL = f'{URLS.MAIN_URL}{URLS.CREATE_ORDER}'

    @allure.title('Проверка на получение списка заказов')
    def test_list_order_without_parametrs(self):
        response = requests.get(self.API_URL)
        assert len(response.json()['orders']) > 0
