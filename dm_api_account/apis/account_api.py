import requests


class AccountApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            user_token
    ):
        """
        Activate registered user
        :param user_token:
        :return:
        """
        headers = {
            'accept': 'test/plain'
        }
        response = requests.put(
            url=f'{self.host}/v1/account/{user_token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change register user email
        :param json_data:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
        return response
