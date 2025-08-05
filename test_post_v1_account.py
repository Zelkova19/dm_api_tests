import requests


def test_post_v1_account():
    # Регистрация полльзователя

    login = 'vmenshikov_test'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получить письма из почтового сервера

    params = {
        'limit': '50'
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    #  Получить активационный токен

    ...

    #  Активация пользователя
    headers = {
        'accept': 'test/plain'
    }

    response = requests.get('http://5.63.153.31:5051/v1/account/dd4ed1b4-0f8c-4e65-8447-271fb81eeee1', headers=headers)
    print(response.status_code)
    print(response.text)

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }


    response = requests.get('http://5.63.153.31:5051/v1/account/dd4ed1b4-0f8c-4e65-8447-271fb81eeee1', json=json_data)
    print(response.status_code)
    print(response.text)

