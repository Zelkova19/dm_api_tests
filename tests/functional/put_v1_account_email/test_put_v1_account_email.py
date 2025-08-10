import time
from json import loads
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # Регистрация полльзователя
    account_api = AccountApi(host='http://5.63.153.31:5051/')
    login_api = LoginApi(host='http://5.63.153.31:5051/')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025/')

    faker = Faker()
    login = faker.name().replace(' ', '')
    password = faker.password()
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Письмо не получено'

    #  Получить активационный токен

    user_token = get_activation_token_by_login(login, response)

    assert user_token is not None, 'Ожидали токен, получили None'

    #  Активация пользователя

    response = account_api.put_v1_account_token(user_token=user_token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был активирован'

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был авторизован'

    # Меняем email
    json_data = {
        'login': login,
        'password': password,
        'email': f'new_{login}@mail.ru'
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, f'Email не был изменен, пришло {response.json()}'

    # Повторная авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, f'Ожидали Forbidden, пришло {response.json()}'

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Письмо не получено'

    #  Получить активационный токен

    user_token = get_activation_token_by_login(login, response)

    assert user_token is not None, 'Ожидали токен, получили None'

    #  Активация пользователя

    response = account_api.put_v1_account_token(user_token=user_token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был активирован'

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f'Пользователь не был авторизован'


def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        try:
            user_data = loads(item['Content']['Body'])
        except KeyError:
            continue

        user_login = user_data.get('Login')
        if user_login == login:
            link = user_data.get('ConfirmationLinkUrl')
            if link:
                token = link.split('/')[-1]
                return token
    return None
