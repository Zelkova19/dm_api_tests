import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            token = function(*args, **kwargs)
            count += 1
            print(f'Попыток получить токен = {count}!')
            if count == 5:
                raise AssertionError('Превышено количество попыток активационного токена!')
            if token:
                return token
            time.sleep(1)
        return None

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login': login, 'password': password}
        )
        token = {'x-dm-auth-token': response.headers['x-dm-auth-token']}

        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def change_password(
            self,
            login: str,
            email: str,
            password: str,
            new_password: str
    ):
        user = self.user_login(login=login, password=password)
        response = self.dm_account_api.account_api.post_v1_account_password(
            json={
                'login': login,
                'email': email
            },
            headers={
                'x-dm-auth-token': user.headers['x-dm-auth-token']
            }
        )
        assert response.status_code == 200, f'Пришло {response.status_code}, {response.json()}'

        token = self.get_token(
            login=login,
            token_type='reset'
        )
        self.dm_account_api.account_api.put_v1_account_password(
            json={
                'login': login,
                'oldPassword': password,
                'newPassword': new_password,
                'token': token
            }
        )
        assert response.status_code == 200, f'Пришло {response.status_code}, {response.json()}'

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан {response.text}'
        token = self.get_token(login=login)
        assert token is not None, 'Ожидали токен, получили None'
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        assert response.status_code == 200, f'Пользователь не был активирован'
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):

        json_data = {
            'login': login,
            'password': password,
            'remember_me': remember_me
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f'Пользователь не был авторизован'
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'email': new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f'Email не был изменен, пришло {response.json()}'

        json_data = {
            'login': login,
            'password': password,
            'remember_me': remember_me
        }

        token = self.get_token(login=login)
        assert token is not None, 'Ожидали токен, получили None'
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        assert response.status_code == 200, f'Пользователь не был активирован'
        return response

    @retrier
    def get_token(
            self,
            login,
            token_type='activation'
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except KeyError:
                continue

            user_login = user_data['Login']
            activation_token = user_data.get('ConfirmationLinkUrl')
            reset_token = user_data.get('ConfirmationLinkUri')
            if user_login == login and activation_token and token_type == 'activation':
                token = activation_token.split('/')[-1]
            elif user_login == login and reset_token and token_type == 'reset':
                token = reset_token.split('/')[-1]

        return token
