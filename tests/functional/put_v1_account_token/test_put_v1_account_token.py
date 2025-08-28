import allure


@allure.suite("Проверка метода POST V1/account/token")
class TestsPostV1AccountToken:
    @allure.title("Проверка получения токена")
    def test_post_v1_account_token(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
