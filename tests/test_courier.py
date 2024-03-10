import allure
import pytest
import requests

from data import Courier
from generator import generate_new_courier_data
from urls import URLS


class TestCreateCourier:
    API_URL = f'{URLS.MAIN_URL}{URLS.CREATE_COURIER}'

    @allure.title('Проверка на успешное создание курьера')
    def test_create_courier_pass(self):
        payload = generate_new_courier_data()
        response_text = '{"ok":true}'
        response = requests.post(self.API_URL, data=payload)
        assert response.status_code == 201 and response.text == response_text

    @allure.title('Проверка на создание двух одинаковых курьеров с одинаковыми логинами')
    def test_courier_double_login(self):
        payload_first, payload_second = generate_new_courier_data(double_login=True)
        # Создаем 1ого курьера
        response1 = requests.post(self.API_URL, data=payload_first)
        # Отправляем запрос на создание 2ого
        response2 = requests.post(self.API_URL, data=payload_first)
        assert (response1.status_code == 201 and
                response2.status_code == 409 and 'Этот логин уже используется' in response2.text)

    @allure.title('Проверка на создание курьера без логина (негативный тест)')
    def test_create_courier_without_login(self):
        payload = generate_new_courier_data(login=False)
        response = requests.post(self.API_URL, data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для создания учетной записи' in response.text

    @allure.title('Проверка на создание курьера без пароля (негативный тест)')
    def test_create_courier_without_password(self):
        payload = generate_new_courier_data(password=False)
        response = requests.post(self.API_URL, data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для создания учетной записи' in response.text


class TestLoginCourier:
    API_URL = f'{URLS.MAIN_URL}{URLS.LOGIN_COURIER}'

    @allure.title('Проверка на Авторизацию под курьером: выдает id')
    def test_courier_login_pass(self):
        response = requests.post(self.API_URL, data=Courier.data_login_password_pass)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка на авторизацию, если логин или пароль неккорректный')
    @pytest.mark.parametrize('data',
                             [Courier.data_login_pass_password_fail,
                              Courier.data_login_fail_password_pass])
    def test_courier_login_negative(self, data):
        response = requests.post(self.API_URL, data=data)
        assert response.status_code == 404 and 'Учетная запись не найдена' in response.text

    @pytest.mark.parametrize('data',
                             [Courier.data_without_login,
                              Courier.data_without_password])
    @allure.title('Проверка на ошибку при авторизации, если не заполнить логин или пароль')
    def test_courier_login_witout_required_data(self, data):
        response = requests.post(self.API_URL, data=data)
        assert response.status_code == 400 and 'Недостаточно данных для входа' in response.text
