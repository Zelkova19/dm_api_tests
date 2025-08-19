from dm_api_account.models.registration import Registration
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelop
from rest_client.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :param:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def get_v1_account(
            self,
            validate_response=True,
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
        if validate_response:
            return UserDetailsEnvelope(**response.json())
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
        UserEnvelop(**response.json())
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
        UserEnvelop(**response.json())
        return response

    def put_v1_account_token(
            self,
            user_token,
            validate_response=True
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
        if validate_response:
            return UserEnvelop(**response.json())
        return response

    def put_v1_account_email(
            self,
            json_data,
            validate_response=True
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
        if validate_response:
            return UserEnvelop(**response.json())
        return response
