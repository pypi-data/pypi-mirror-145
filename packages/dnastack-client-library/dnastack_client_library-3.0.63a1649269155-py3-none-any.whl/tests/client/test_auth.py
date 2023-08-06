import time
from uuid import uuid4

from dnastack import DataConnectClient
from dnastack.auth.authorizers import ClientCredentialsAuth, PersonalAccessTokenAuth
from dnastack.configuration import Authentication, ServiceEndpoint, Oauth2Authentication
from dnastack.helpers.environments import env
from ..exam_helper import token_endpoint, client_secret, client_id, \
    authorization_endpoint, personal_access_endpoint, redirect_url, ExtendedBaseTestCase


class TestAuthentication(ExtendedBaseTestCase):
    """
    Test authentication flows

    .. note:: The URL used in the authorization tests are fake.
    """

    test_resource_url = env('E2E_PROTECTED_DATA_CONNECT_URL', default='https://data-connect-trino.viral.ai/')

    def test_client_credentials_flow(self):
        test_endpoint = self.__create_endpoint(
            client_id=client_id,
            client_secret=client_secret,
            grant_type='client_credentials',
            resource_url=self.test_resource_url,
            token_endpoint=token_endpoint
        )

        auth = ClientCredentialsAuth(test_endpoint)
        auth.authorize('https://dnastack.com')
        auth_session = auth.session
        self.assertIsNotNone(auth_session)
        self.assertIsNotNone(auth_session.config_hash)
        self.assert_not_empty(auth_session.access_token, 'empty access token')
        self.assertIsNone(auth_session.refresh_token, 'non-empty refresh token')
        self.assertGreater(auth_session.valid_until, 0)

        # As the OAuth server may respond too quickly, this is to ensure that the expiry times are different.
        time.sleep(1)

        # Reauthorize the endpoint with updated config
        test_endpoint.authentication.oauth2.redirect_url = 'https://dnastack.com/'
        auth.authorize('https://dnastack.com')
        refreshed_auth_session = auth.session
        self.assertIsNotNone(refreshed_auth_session)
        self.assertIsNotNone(refreshed_auth_session.config_hash)
        self.assert_not_empty(refreshed_auth_session.access_token, 'empty access token')
        self.assertIsNone(refreshed_auth_session.refresh_token, 'non-empty refresh token')
        self.assertGreater(refreshed_auth_session.valid_until, 0)

        # Check that the session has been refreshed when the auth info is updated.
        self.assertNotEqual(refreshed_auth_session, auth_session)
        self.assertNotEqual(refreshed_auth_session.config_hash, auth_session.config_hash)
        self.assertNotEqual(refreshed_auth_session.access_token, auth_session.access_token)
        self.assertGreater(refreshed_auth_session.valid_until, auth_session.valid_until)


    def test_personal_access_token_flow(self):
        email = env('E2E_AUTH_TEST_PAT_EMAIL')
        token = env('E2E_AUTH_TEST_PAT_TOKEN')

        if not email or not token:
            self.skipTest('The PAT flow test does not have both email and token.')

        auth = PersonalAccessTokenAuth(self.__create_endpoint(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            grant_type='authorization_code',
            personal_access_endpoint=personal_access_endpoint,
            personal_access_email=email,
            personal_access_token=token,
            redirect_url=redirect_url,
            resource_url=self.test_resource_url,
            token_endpoint=token_endpoint,
        ))
        auth.authorize('https://dnastack.com')
        auth_session = auth.session
        self.assertIsNotNone(auth_session)
        self.assert_not_empty(auth_session.access_token, 'empty access token')
        self.assert_not_empty(auth_session.refresh_token, 'empty refresh token')
        self.assertGreater(auth_session.valid_until, 0)

    def __create_endpoint(self, **kwargs) -> ServiceEndpoint:
        return ServiceEndpoint(
            id=f'auto-test-{uuid4()}',
            adapter_type=DataConnectClient.get_adapter_type(),
            url=self.test_resource_url,
            authentication=Authentication(oauth2=Oauth2Authentication(**kwargs)),
        )
