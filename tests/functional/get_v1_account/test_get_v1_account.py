import allure

from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


@allure.suite("Тесты на проверку метода GET V1/account")
class TestsGetV1Account:

    @allure.sub_suite("Позитивные тесты")
    @allure.title("Авторизованный запрос пользователя")
    def test_get_v1_account_auth(
            self,
            auth_account_helper
    ):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.get_v1_account(response=response, login_suffix='Roman')

    @allure.sub_suite("Негативные тесты")
    @allure.title("Неавторизованный запрос пользователя")
    def test_get_v1_account_no_auth(
            self,
            account_helper
    ):
        with check_status_code_http(expected_status_code=401, expected_message='User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account()
