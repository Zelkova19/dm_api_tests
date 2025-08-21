from datetime import datetime

import pytest
from faker import Faker
from hamcrest import assert_that, has_property, ends_with, all_of, instance_of, has_properties, equal_to

from checkers.http_checkers import check_status_code_http
from conftest import prepare_user

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
    assert_that(response, all_of(
        has_property('resource', has_property('login', ends_with('Roman'))),
        has_property('resource', has_property('registration', instance_of(datetime))),
        has_property('resource',
                     has_properties
                        (
                            {"rating": has_properties
                                (
                                    {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                    }
                                )
                            }
                        )
                    )
                )
            )

    print(response)
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
