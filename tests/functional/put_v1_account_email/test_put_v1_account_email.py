import allure


@allure.suite("Проверка метода PUT V1/account.email")
class TestPutV1AccountEmail:

    @allure.title("Проверка семны почты")
    def test_put_v1_account_email(self, account_helper, prepare_user):

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)

        # Меняем email
        new_email = f'new_{login}@mail.ru'
        account_helper.change_email(login=login, password=password, new_email=new_email)
        account_helper.user_login(login=login, password=password)
