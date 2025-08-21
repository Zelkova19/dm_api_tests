from checkers.http_checkers import check_status_code_http


def test_delete_v1_account_login_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 204


def test_delete_v1_account_login_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.login_api.delete_v1_account_login()
