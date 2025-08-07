from json import loads

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


def test_post_v1_account_login():

    account_api = AccountApi(host='http://5.63.153.31:5051/')
    login_api = LoginApi(host='http://5.63.153.31:5051/')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025/')

    # Подготовка пользователя

    login = 'vmenshikov_test_ro_52'
    password = '123456789'
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
    user_token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            user_token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(user_token)
    return user_token
