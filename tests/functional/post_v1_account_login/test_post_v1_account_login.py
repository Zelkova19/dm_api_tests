import time
from json import loads
from faker import Faker

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


def test_post_v1_account_login():

    account_api = AccountApi(host='http://5.63.153.31:5051/')
    login_api = LoginApi(host='http://5.63.153.31:5051/')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025/')

    # Подготовка пользователя

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
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f'Письмо не получено'

    user_token = get_activation_token_by_login(login, response)
    assert user_token is not None, 'Ожидали токен, получили None'

    response = account_api.put_v1_account_token(user_token=user_token)
    assert response.status_code == 200, f'Пользователь не был активирован'

    # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.json())
    assert response.status_code == 200, f'Пользователь не был авторизован'
    assert response.json()['resource']['login'] == login

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
