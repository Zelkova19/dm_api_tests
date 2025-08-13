import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

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
        token = self.get_activation_token_by_login(login=login)
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




        token = self.get_activation_token_by_login(login=login)
        assert token is not None, 'Ожидали токен, получили None'
        response = self.dm_account_api.account_api.put_v1_account_token(user_token=token)
        assert response.status_code == 200, f'Пользователь не был активирован'
        return response

    def get_activation_token_by_login(
            self,
            login
            ):
        token = None
        time.sleep(3)  # penalty get message
        response = self.mailhog.mailhog_api.get_api_v2_messages()
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
        return token
