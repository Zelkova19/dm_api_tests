from collections import namedtuple

import pytest

from helpers.account_helper import AccountHelper
from tests.functional import *

import structlog

from rest_client.configuration import Configuration as MailhogConfiguration
from rest_client.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def account_helper(
        mailhog_api,
        account_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def auth_account_helper(
        mailhog_api,
        prepare_user
):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.register_new_user(login=prepare_user.login, password=prepare_user.password, email=prepare_user.email)
    account_helper.auth_client(
        login=prepare_user.login,
        password=prepare_user.password
    )
    return account_helper


@pytest.fixture
def prepare_user():
    faker = Faker()
    login = faker.name().replace(' ', '') + 'Roman'
    password = faker.password()
    email = f'{login}@mail.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user

