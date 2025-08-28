import allure


@allure.suite("Проверка метода POST V1/account/password")
class TestsPostV1AccountPassword:

    @allure.title("Проверка смены пароля")
    def test_post_v1_account_password(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_password = "011235813"
        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_password(login=login, email=email, password=password, new_password=new_password)
        account_helper.user_login(login=login, password=new_password)
