import time
from json import JSONDecodeError, loads

import allure

from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
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

    @allure.step("Авторизация пользователя")
    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)
        token = {'x-dm-auth-token': response.headers['x-dm-auth-token']}

        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    @allure.step("Смена пароля")
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

    @allure.step('Регистрация нового пользователя')
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):

        registration = Registration(
            login=login,
            password=password,
            email=email
        )

        self.dm_account_api.account_api.post_v1_account(registration=registration)
        start_time = time.time()
        token = self.get_token(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, f'Время получения токена превысило 3 секунды. Время выполнения {end_time - start_time}'
        assert token is not None, 'Ожидали токен, получили None'
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        return response

    @allure.step('Аутентификация пользователя')
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):

        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers['x-dm-auth-token'], 'Токен для пользователя не был получен'
        return response

    @allure.step("Смена почты")
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
        self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)

        json_data = {
            'login': login,
            'password': password,
            'remember_me': remember_me
        }

        token = self.get_token(login=login)
        assert token is not None, 'Ожидали токен, получили None'
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
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
            except (JSONDecodeError, KeyError):
                continue

            user_login = user_data['Login']
            activation_token = user_data.get('ConfirmationLinkUrl')
            reset_token = user_data.get('ConfirmationLinkUri')
            if user_login == login and activation_token and token_type == 'activation':
                token = activation_token.split('/')[-1]
            elif user_login == login and reset_token and token_type == 'reset':
                token = reset_token.split('/')[-1]

        return token
