import copy
import random
import string


def generate_new_courier_data(login=True, password=True, first_name=True, double_login=False):
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    payload_first = {}

    # генерируем логин, пароль и имя курьера
    if login:
        login = generate_random_string(10)
        payload_first['login'] = login
    if password:
        password = generate_random_string(10)
        payload_first['password'] = password
    if first_name:
        first_name = generate_random_string(10)
        payload_first['firstName'] = first_name

    if double_login:
        payload_second = {}
        payload_second['login'] = copy.deepcopy(payload_first['login'])
        payload_second['password'] = payload_first['password'][::-1]
        payload_second['firstName'] = payload_first['firstName'][::-1]
        return payload_first, payload_second
    return payload_first
