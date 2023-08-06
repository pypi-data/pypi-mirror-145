"""CLI 'list' command test module"""

# standard
import json
from uuid import uuid4
# external
import requests_mock
# local
from matatika.cli.commands.root import matatika
from matatika.context import CONTEXTS
from matatika.exceptions import VariableNotSetError
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import DATASET, not_found


class TestCLIGet(TestCLI):
    """Test class for CLI get command"""

    def test_get_no_subcommmand(self):
        """Test get with no subcommand"""

        result = self.runner.invoke(matatika, ["get"])
        self.assertIs(result.exit_code, 0)
        self.assertIn(
            "Usage: matatika get [OPTIONS] COMMAND [ARGS]...", result.output)

    def test_get_invalid_subcommand(self):
        """Test get with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["get", resource_type])
        self.assertIs(result.exit_code, 2)
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)

    @requests_mock.Mocker()
    def test_get_dataset_by_id(self, mock: requests_mock.Mocker):
        """Test get dataset by ID"""

        mock.get(requests_mock.ANY, status_code=200, json=DATASET)

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               str(uuid4())])

        self.assertIs(result.exit_code, 0)
        self.assertIn(json.dumps(DATASET), result.output)

    @requests_mock.Mocker()
    def test_get_dataset_by_alias(self, mock: requests_mock.Mocker):
        """Test get dataset by alias"""

        mock.get(requests_mock.ANY, status_code=200, json=DATASET)

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               "alias",
                                               "-w",
                                               str(uuid4())])
        self.assertIs(result.exit_code, 0)
        self.assertIn(json.dumps(DATASET), result.output)

    def test_get_dataset_by_alias_no_workspace_id(self):
        """Test get dataset by alias without specifying a workspace ID"""

        self.mock__read_json.return_value[CONTEXTS]['context1']['workspace_id'] = None

        workspace_id_not_set_msg = str(VariableNotSetError('WORKSPACE_ID'))

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               invalid_alias])
        self.assertIs(result.exit_code, 1)
        self.assertIn(workspace_id_not_set_msg, result.output)

    @requests_mock.Mocker()
    def test_get_dataset_by_invalid_alias(self, mock: requests_mock.Mocker):
        """Test get dataset by an invalid dataset alias"""

        invalid_alias = 'invalid-alias'
        mock_json = not_found(invalid_alias)
        mock.get(requests_mock.ANY, status_code=404, json=mock_json)

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               invalid_alias,
                                               "-w",
                                               str(uuid4())])
        self.assertIs(result.exit_code, 1)
        self.assertIn(mock_json['message'], result.output)
