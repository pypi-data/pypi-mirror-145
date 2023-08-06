"""Catalog test module"""

# standard
from unittest.case import TestCase
from unittest.mock import Mock, patch
# external
import requests_mock
# local
from matatika.catalog import Catalog
from matatika.library import MatatikaClient
from tests.api_response_mocks import PROFILES


class TestCatalog(TestCase):
    """Test class for catalog operations"""

    @patch('matatika.catalog.get_access_token')
    def test_new_access_token_given_no_access_token(self, mock_get_access_token: Mock):
        """Test new access token given `client_id`, `client_secret` and no `auth_token`"""

        access_token = 'access_token'
        mock_get_access_token.return_value = access_token

        client = MatatikaClient(None, 'client_id', 'client_secret')
        Catalog(client)

        mock_get_access_token.assert_called_once()
        self.assertIs(client.auth_token, access_token)

    @patch('matatika.catalog.get_access_token')
    def test_no_new_access_token_given_access_token(self, mock_get_access_token: Mock):
        """Test no new access token given `auth_token`"""

        access_token = 'access_token'
        mock_get_access_token.return_value = access_token

        client = MatatikaClient(access_token)
        Catalog(client)

        mock_get_access_token.assert_not_called()

    @patch('matatika.catalog.get_access_token')
    @requests_mock.Mocker()
    def test_new_access_token_on_401(self,
                                     mock_get_access_token: Mock,
                                     mock: requests_mock.Mocker):
        """Test new access token logic when response `401 Unauthorized`"""

        access_token = 'access_token'
        mock_get_access_token.return_value = access_token

        mock.get(requests_mock.ANY, [
            {'status_code': 401},
            {'status_code': 200, 'json': PROFILES}
        ])

        client = MatatikaClient(access_token)
        catalog = Catalog(client)
        catalog.get_profile()

        mock_get_access_token.assert_called_once()
        self.assertIs(client.auth_token, access_token)

        mock_get_access_token.reset_mock()

        catalog.get_profile()
        mock_get_access_token.assert_not_called()
