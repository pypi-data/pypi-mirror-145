"""catalog module"""

import requests
from requests.models import Response
from matatika.auth import get_access_token
from matatika.exceptions import MatatikaException
from matatika.types import DataFormat
from matatika.dataset import Dataset
from matatika.channel import Channel


class Catalog:  # pylint: disable=too-many-instance-attributes
    """Class to handle client-side HTTP requests to the Matatika API"""

    def _update_auth_token(self):
        self.client.auth_token = get_access_token(self.client.client_id,
                                                  self.client.client_secret,
                                                  self.client.endpoint_url)

    def _refresh_access_token(self, response: Response, *_args, **_kwargs):
        if response.status_code != 401:
            return None

        self._update_auth_token()

        self.session.headers['Authorization'] = f'Bearer {self.client.auth_token}'
        response.request.headers.update(self.session.headers)
        response.request.deregister_hook(
            'response', self._refresh_access_token)

        return self.session.send(response.request)

    @staticmethod
    def _raise_for_status(response: Response, *_args, **_kwargs):
        if response.status_code == 404:
            raise MatatikaException(response.json()['message'])

        response.raise_for_status()

    def __init__(self, client):

        self.client = client

        if not client.auth_token:
            self._update_auth_token()

        self.profiles_url = client.endpoint_url + '/profiles'
        self.workspaces_url = client.endpoint_url + '/workspaces'
        self.datasets_url = client.endpoint_url + '/datasets'
        self.workspace_channels_url = f'{self.workspaces_url}/{client.workspace_id}/channels/'
        self.workspace_datasets_url = f'{self.workspaces_url}/{client.workspace_id}/datasets'

        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {client.auth_token}',
                                'content-type': 'application/json'}
        self.session.hooks['response'] = [
            self._refresh_access_token,
            self._raise_for_status
        ]

    def post_resources(self, resources):
        """Publishes a converted yaml file into a workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        publish_responses = []

        for resource in resources:
            if isinstance(resource, Dataset):
                response = self.session.post(self.workspace_datasets_url,
                                             data=resource.to_json_str())
            elif isinstance(resource, Channel):
                response = self.session.put(self.workspace_channels_url + resource.name,
                                            data=resource.to_json_str())

            publish_responses.append(response)

        return publish_responses

    def get_workspaces(self):
        """Returns all workspaces the user profile is a member of"""

        workspaces = self.session.get(self.workspaces_url).json()

        try:
            return workspaces['_embedded']['workspaces']
        except KeyError:
            return []

    def get_datasets(self):
        """Returns all datasets in the supplied workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        datasets = self.session.get(self.workspace_datasets_url).json()

        try:
            return datasets['_embedded']['datasets']
        except KeyError:
            return []

    def get_channels(self):
        """Returns all channels in the supplied workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        channels = self.session.get(self.workspace_channels_url).json()

        try:
            return channels['_embedded']['channels']
        except KeyError:
            return []

    def get_profile(self):
        """Returns the user profile"""

        return self.session.get(self.profiles_url).json()['_embedded']['profiles'][0]

    def get_data(self, id_, data_format: DataFormat):
        """Returns the data from a dataset"""

        if data_format is DataFormat.CSV:
            self.session.headers['Accept'] = 'text/csv'

        return self.session.get(f'{self.datasets_url}/{id_}/data').text

    def get_dataset(self, id_):
        """Returns a dataset"""

        return self.session.get(f'{self.datasets_url}/{id_}').json()

    def get_workspace_dataset(self, id_or_alias):
        """Returns a workspace dataset"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        return self.session.get(self.workspace_datasets_url + f'/{id_or_alias}').json()

    def delete_dataset(self, id_):
        """Deletes a dataset"""

        self.session.delete(f'{self.datasets_url}/{id_}')

    def delete_workspace(self, id_):
        """Deletes a workspace"""

        self.session.delete(f'{self.workspaces_url}/{id_}')
