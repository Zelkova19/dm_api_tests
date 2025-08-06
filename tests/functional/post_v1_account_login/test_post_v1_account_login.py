import pprint
from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account_login():
    login_api = LoginApi(host='http://5.63.153.31:5051/')

    login = 'vmenshikov_test_ro_13'
    password = '123456789'

    # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    pprint.pprint(response.json())
    assert response.status_code == 200, f'Пользователь не был авторизован'
    assert response.json()['resource']['login'] == login
