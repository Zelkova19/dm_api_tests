import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelop
from rest_client.client import RestClient


class LoginApi(RestClient):

    @allure.step("Аутентификация пользователя с кредами")
    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        """
        Authenticate via credentials
        :param:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelop(**response.json())
        return response

    @allure.step("Выход из аккаунта")
    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Logout as current user
        :param :
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    @allure.step("Выход мз всех устройств")
    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :param :
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response
