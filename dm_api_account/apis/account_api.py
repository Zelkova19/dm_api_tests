from rest_client.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def post_v1_account_password(
            self,
            **kwargs
    ):
        """
        Reset registered user password
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            **kwargs
        )
        return response

    def put_v1_account_password(
            self,
            **kwargs
    ):
        """
        Change registered user password
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            **kwargs
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
        response = self.put(
            path=f'/v1/account/{user_token}',
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
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response
