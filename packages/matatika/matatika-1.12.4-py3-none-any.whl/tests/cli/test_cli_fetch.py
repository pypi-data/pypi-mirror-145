"""CLI 'fetch' command test module"""

# standard
import unittest
from unittest.mock import patch
from uuid import uuid4
# external
import requests_mock
# local
from matatika.cli.commands.root import matatika
from matatika.cli.variables import VariableType
from matatika.context import CONTEXTS
from matatika.exceptions import VariableNotSetError
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import DATA, DATA_CSV, DATASET, not_found


class TestCLIFetch(TestCLI):
    """Test class for CLI fetch command"""

    def test_fetch_without_dataset_id_or_alias_argument(self):
        """Test fetch without dataset ID or alias argument"""

        result = self.runner.invoke(matatika, ["fetch"])
        self.assertIs(result.exit_code, 2)
        self.assertIn(
            "Error: Missing argument 'DATASET_ID_OR_ALIAS'.", result.output)

    @requests_mock.Mocker()
    def test_fetch_by_invalid_dataset_id(self, mock: requests_mock.Mocker):
        """Test fetch by an invalid dataset ID"""

        invalid_uuid = str(uuid4())
        mock_json = not_found(invalid_uuid)
        mock.get(requests_mock.ANY, status_code=404, json=mock_json)

        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_uuid])
        self.assertIs(result.exit_code, 1)
        self.assertIn(mock_json['message'], result.output)

    @requests_mock.Mocker()
    def test_fetch_by_invalid_alias(self, mock: requests_mock.Mocker):
        """Test fetch by an invalid dataset alias"""

        invalid_alias = 'invalid-alias'
        mock_json = not_found(invalid_alias)
        mock.get(requests_mock.ANY, status_code=404, json=mock_json)

        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_alias,
                                               "-w",
                                               str(uuid4())])
        self.assertIs(result.exit_code, 1)
        self.assertIn(mock_json['message'], result.output)

    def test_fetch_by_alias_no_workspace_id(self):
        """Test fetch by dataset alias without specifying a workspace ID"""

        self.mock__read_json.return_value[CONTEXTS]['context1']['workspace_id'] = None

        workspace_id_not_set_msg = str(
            VariableNotSetError(VariableType.WORKSPACE_ID.name))

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_alias])
        self.assertIs(result.exit_code, 1)
        self.assertIn(workspace_id_not_set_msg, result.output)

    @requests_mock.Mocker()
    def test_fetch_by_id(self, mock: requests_mock.Mocker):
        """Test fetch with dataset ID"""

        uuid = DATASET.get('id')
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': DATASET},
            {'status_code': 200, 'text': str(DATA)}
        ])

        result = self.runner.invoke(matatika, ["fetch",
                                               uuid])
        self.assertIs(result.exit_code, 0)
        self.assertIn(str(DATA), result.output)

    @requests_mock.Mocker()
    def test_fetch_by_alias(self, mock: requests_mock.Mocker):
        """Test fetch with dataset ID"""

        uuid = DATASET.get('id')
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': DATASET},
            {'status_code': 200, 'text': str(DATA)}
        ])

        result = self.runner.invoke(matatika, ["fetch",
                                               "alias",
                                               "-w",
                                               uuid])
        self.assertIs(result.exit_code, 0)
        self.assertIn(str(DATA), result.output)

    @requests_mock.Mocker()
    def test_fetch_as_csv(self, mock: requests_mock.Mocker):
        """Test fetch with dataset ID"""

        uuid = DATASET.get('id')
        mock.get(f'/api/datasets/{uuid}', status_code=200, json=DATASET)
        mock.get(f'/api/datasets/{uuid}/data', status_code=200, text=DATA_CSV)

        result = self.runner.invoke(matatika, ["fetch",
                                               uuid,
                                               "--as",
                                               "csv"])
        self.assertIs(result.exit_code, 0)
        self.assertIn(DATA_CSV, result.output)

    @unittest.skip
    @patch('cli.commands.fetch.open')
    @requests_mock.Mocker()
    def test_fetch_with_output_file_opt(self, mock: requests_mock.Mocker, _mock_open):
        """Test fetch with output file option"""

        mock.get(requests_mock.ANY, status_code=200, text=str(DATA))

        dataset_id = str(uuid4())

        file_ = "test.txt"
        result = self.runner.invoke(matatika, ["fetch",
                                               dataset_id,
                                               "-f", file_])
        self.assertIs(result.exit_code, 0)
        self.assertIn(f"Dataset {dataset_id} data successfully written to {file_}",
                      result.output)
