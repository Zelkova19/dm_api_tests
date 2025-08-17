def test_delete_v1_account_login_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 204


def test_delete_v1_account_login_no_auth(
        account_helper
):
    response = account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 401
