import time
from json import loads

import structlog
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from rest_client.configuration import Configuration as MailhogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


def test_post_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    faker = Faker()
    login = faker.name().replace(' ', '') + 'token'
    password = faker.password()
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получить письма из почтового сервера

    time.sleep(3) # penalty get message

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f'Письмо не получено'

    #  Получить активационный токен

    user_token = get_activation_token_by_login(login, response)

    assert user_token is not None, 'Ожидали токен, получили None'

    #  Активация пользователя

    response = account_api.put_v1_account_token(user_token=user_token)
    assert response.status_code == 200, f'Пользователь не был активирован'


def get_activation_token_by_login(
        login,
        response
        ):
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
