import os
from collections import namedtuple
from pathlib import Path

from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

import pytest

from helpers.account_helper import AccountHelper
from tests.functional import *

import structlog

from packages.rest_client.configuration import Configuration as MailhogConfiguration
from packages.rest_client.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.token'
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()

@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
        ):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")
    request.config.stash["telegram-notifier-addfields"]["enviroment"] = config_name
    request.config.stash["telegram-notifier-addfields"]["report"] = "https://zelkova19.github.io/dm_api_tests/"


def pytest_addoption(
        parser
        ):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get('service.mailhog'))
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
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
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
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
