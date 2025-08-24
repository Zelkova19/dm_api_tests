import pytest

from faker import Faker
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

faker = Faker()

def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)
    account_helper.user_login(login=login, password=password)


@pytest.mark.parametrize('login, email, password, status_code, error_message',
                         [(faker.name(), faker.email(), '12345', 400, 'Validation failed'),
                          (faker.name(), 'user.ru', faker.password(), 400, 'Validation failed'),
                          ('U', faker.email(), faker.password(), 400, 'Validation failed')])
def test_post_v1_account_validation_filed(
        account_helper,
        prepare_user,
        login,
        email,
        password,
        error_message,
        status_code
):

    with check_status_code_http(status_code, error_message):
        account_helper.register_new_user(login=login, password=password, email=email)
