"""CLI 'delete' command test module"""

# standard
from uuid import uuid4
# external
import requests_mock
# local
from matatika.cli.commands.root import matatika
from tests.api_response_mocks import not_found
from tests.cli.test_cli import TestCLI


class TestCLIDelete(TestCLI):
    """Test class for CLI delete command"""

    def test_delete_no_subcommand(self):
        """Test delete with no subcommand"""

        result = self.runner.invoke(matatika, ["delete"])
        self.assertIs(result.exit_code, 0)

        expected_message = "Usage: matatika delete [OPTIONS] COMMAND [ARGS]..."
        self.assertIn(expected_message, result.output)

    def test_delete_invalid_subcommand(self):
        """Test delete with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["delete", resource_type])
        self.assertIs(result.exit_code, 2)

        expected_message = f"Error: No such command '{resource_type}'."
        self.assertIn(expected_message, result.output)


class TestCLIDeleteWorkspace(TestCLI):
    """Test class for CLI delete workspaces command"""

    def test_delete_workspaces_no_arguments(self):
        """Test command error when no workspace ID arguments are not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces"])
        self.assertIs(result.exit_code, 2)

        expected_message = "Missing argument 'WORKSPACE_IDS...'"
        self.assertIn(expected_message, result.output)

    def test_delete_workspaces_confirm_no(self):
        """Test workspace is not deleted after rejected client confirmation"""

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='n')
        self.assertIs(result.exit_code, 0)

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

    @requests_mock.Mocker()
    def test_delete_workspaces_confirm_yes(self, mock: requests_mock.Mocker):
        """Test workspace is deleted after client confirmation"""

        mock.delete(requests_mock.ANY, status_code=204)

        workspace_id = str(uuid4())
        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')
        self.assertIs(result.exit_code, 0)

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted workspace(s): {workspace_id}"
        self.assertIn(expected_message, result.output)

    @requests_mock.Mocker()
    def test_delete_workspaces_bypass_confirm(self, mock: requests_mock.Mocker):
        """Test workspace is deleted with no client confirmation"""

        mock.delete(requests_mock.ANY, status_code=204)

        workspace_id = str(uuid4())
        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "workspaces",
                                               workspace_id])
        self.assertIs(result.exit_code, 0)

        expected_message = f"Successfully deleted workspace(s): {workspace_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

    @requests_mock.Mocker()
    def test_delete_workspaces_not_found(self, mock: requests_mock.Mocker):
        """Test workspace is not found when trying to delete"""

        workspace_id = str(uuid4())
        mock_json = not_found(workspace_id)
        mock.delete(requests_mock.ANY, status_code=404, json=mock_json)

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')
        self.assertIs(result.exit_code, 1)
        self.assertIn(mock_json['message'], result.output)

    @requests_mock.Mocker()
    def test_delete_workspaces_server_error(self, mock: requests_mock.Mocker):
        """Test server error encountered when trying to delete workspace"""

        status_code = 503
        mock.delete(requests_mock.ANY, status_code=status_code)

        workspace_id = str(uuid4())
        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')
        self.assertIs(result.exit_code, 1)

        expected_message = f"{status_code} Server Error"
        self.assertIn(expected_message, result.output)

    @requests_mock.Mocker()
    def test_delete_workspaces_multiple(self, mock: requests_mock.Mocker):
        """Test delete of multiple workspaces"""

        mock.delete(requests_mock.ANY, status_code=204)

        workspace1_id = str(uuid4())
        workspace2_id = str(uuid4())
        workspace3_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "workspaces",
                                               workspace1_id,
                                               workspace2_id,
                                               workspace3_id])
        self.assertIs(result.exit_code, 0)

        expected_message = "Successfully deleted workspace(s): " \
            f"{workspace1_id}, {workspace2_id}, {workspace3_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)


class TestCLIDeleteDataset(TestCLI):
    """Test class for CLI delete dataset command"""

    def test_delete_datasets_no_arguments(self):
        """Test command error when no dataset ID arguments are not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets"])
        self.assertIs(result.exit_code, 2)

        expected_message = "Missing argument 'DATASET_IDS...'"
        self.assertIn(expected_message, result.output)

    def test_delete_datasets_confirm_no(self):
        """Test dataset is not deleted after rejected client confirmation"""

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='n')
        self.assertIs(result.exit_code, 0)

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

    @requests_mock.Mocker()
    def test_delete_datasets_confirm_yes(self, mock: requests_mock.Mocker):
        """Test dataset is deleted after client confirmation"""

        mock.delete(requests_mock.ANY, status_code=204)

        dataset_id = str(uuid4())
        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')
        self.assertIs(result.exit_code, 0)

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted dataset(s): {dataset_id}"
        self.assertIn(expected_message, result.output)

    @requests_mock.Mocker()
    def test_delete_datasets_bypass_confirm(self, mock: requests_mock.Mocker):
        """Test dataset is deleted with no client confirmation"""

        mock.delete(requests_mock.ANY, status_code=204)

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "datasets",
                                               dataset_id])

        expected_message = f"Successfully deleted dataset(s): {dataset_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @requests_mock.Mocker()
    def test_delete_datasets_not_found(self, mock: requests_mock.Mocker):
        """Test dataset is not found when trying to delete"""

        dataset_id = str(uuid4())
        mock_json = not_found(dataset_id)
        mock.delete(requests_mock.ANY, status_code=404, json=mock_json)

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')
        self.assertIs(result.exit_code, 1)
        self.assertIn(mock_json['message'], result.output)

    @requests_mock.Mocker()
    def test_delete_datasets_server_error(self, mock: requests_mock.Mocker):
        """Test server error encountered when trying to delete dataset"""

        status_code = 503
        mock.delete(requests_mock.ANY, status_code=status_code)

        dataset_id = str(uuid4())
        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')

        expected_message = f"{status_code} Server Error"
        self.assertIn(expected_message, result.output)

    @requests_mock.Mocker()
    def test_delete_datasets_multiple(self, mock: requests_mock.Mocker):
        """Test delete of multiple datasets"""

        mock.delete(requests_mock.ANY, status_code=204)

        dataset1_id = str(uuid4())
        dataset2_id = str(uuid4())
        dataset3_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "datasets",
                                               dataset1_id,
                                               dataset2_id,
                                               dataset3_id])

        expected_message = "Successfully deleted dataset(s): " \
            f"{dataset1_id}, {dataset2_id}, {dataset3_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)
