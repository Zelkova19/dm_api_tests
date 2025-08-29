import allure
import pytest

from faker import Faker
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

faker = Faker()

@allure.suite('Тесты на проверку метода POST V1/account')
class TestsPostV1Account:

    @allure.sub_suite('Позитивные тесты')
    @allure.title('Проверка регистрации новго пользователя')
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)

    @allure.sub_suite('Негативные тесты')
    @pytest.mark.parametrize('title, login, email, password, status_code, error_message',
                             [('password', faker.name(), faker.email(), '12345', 400, 'Validation failed'),
                              ('email', faker.name(), 'user.ru', faker.password(), 400, 'Validation failed'),
                              ('login', 'U', faker.email(), faker.password(), 400, 'Validation failed')])
    def test_post_v1_account_validation_filed(
            self,
            account_helper,
            prepare_user,
            login,
            email,
            password,
            error_message,
            status_code,
            title
    ):
        allure.dynamic.title(f'Валидация поля {title}')

        with check_status_code_http(status_code, error_message):
            account_helper.register_new_user(login=login, password=password, email=email)
