from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    GetV1Account.get_v1_account(response=response, login_suffix='Roman')


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(expected_status_code=401, expected_message='User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()
