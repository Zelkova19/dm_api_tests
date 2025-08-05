import pprint

import requests

from json import loads

def test_post_v1_account():
    # Регистрация полльзователя

    login = 'vmenshikov_test113'
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
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получить письма из почтового сервера

    params = {
        'limit': '5'
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'письмо не получено'

    #  Получить активационный токен
    user_token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            user_token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_token)

    assert user_token is not None

    #  Активация пользователя
    headers = {
        'accept': 'test/plain'
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{user_token}', headers=headers)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был активирован'

    # Авторизоваться
    #
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }


    response = requests.post(f'http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был авторизован'

