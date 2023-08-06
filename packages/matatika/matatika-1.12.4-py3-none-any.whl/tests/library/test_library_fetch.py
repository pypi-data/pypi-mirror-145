"""Library 'fetch' method test module"""

# standard
import copy
import json
from uuid import uuid4
# external
import requests_mock
# local
from matatika.exceptions import MatatikaException
from matatika.types import DataFormat
from tests.api_response_mocks import not_found
from tests.library.test_library import TestLibrary

MOCK_DATASET_DATA_RESPONSE = json.dumps([
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 66
    },
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 87
    },
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 149
    }
])

MOCK_DATASET_RESPONSE = {
    'id': 'b1d851b8-cd3c-4047-ad66-2821d7345315',
    'alias': 'w-o-overview-last-30-days',
    'workspaceId': 'a8f504c2-1d44-4d87-9687-5d70cdfce362',
    'title': 'W/O Overview Last 30 days',
    'visualisation': '{"chartjs-chart": {"chartType": "line"}}',
    'metadata': '{"name": "project_sla", "related_table": {"columns": [{"name": "report_year", ' +
                '"label": "Year", "key": "project_sla.report_year"}], "aggregates": [{"name": ' +
                '"total_projects", "label": "Total Work Orders", "key": ' +
                '"project_sla.total_projects"}]}}',
    '_links': {
        'data': {
            'href': 'data-link'
        }
    }
}


class TestLibraryFetch(TestLibrary):
    """Test class for library 'fetch' method"""

    def test_invalid_arg_types(self):
        """Test provided built-in Python type object instances trigger TypeError"""

        for type_ in {int, float, str, tuple, set, list, dict}:
            type_instance = type_()

            with self.assertRaises(TypeError) as ctx:
                self.client.fetch(str(uuid4()), data_format=type_instance)

            error_msg = ctx.exception.__str__()
            print(error_msg)

            self.assertEqual(error_msg,
                             f'DataFormat argument expected, got {type(type_instance).__name__}')

    @requests_mock.Mocker()
    def test_invalid_dataset_id_or_alias(self, mock: requests_mock.Mocker):
        """Test invalid dataset ID or alias raises `MatatikaException`"""

        uuid = str(uuid4())
        mock_json = not_found(uuid)
        mock.get(requests_mock.ANY, status_code=404, json=mock_json)

        with self.assertRaises(MatatikaException) as ctx:
            self.client.fetch(uuid)

        error_msg = ctx.exception.__str__()
        print(error_msg)

        self.assertEqual(error_msg, mock_json['message'])

    @requests_mock.Mocker()
    def test_default(self, mock: requests_mock.Mocker):
        """Test fetch default behaviour"""

        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': MOCK_DATASET_RESPONSE},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        data_py = self.client.fetch(str(uuid4()))

        for mock_data_point, data_point in zip(json.loads(MOCK_DATASET_DATA_RESPONSE), data_py):
            self.assertEqual(list(mock_data_point.values()),
                             list(data_point.values()))

        self.assertIn("Year", data_py[0].keys())
        self.assertIn("Total Work Orders", data_py[0].keys())

    @requests_mock.Mocker()
    def test_default_no_metadata(self, mock: requests_mock.Mocker):
        """Test fetch default behaviour with no metadata"""

        mock_dataset_response_copy = copy.deepcopy(MOCK_DATASET_RESPONSE)
        mock_dataset_response_copy['metadata'] = None
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': mock_dataset_response_copy},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        data_py = self.client.fetch(str(uuid4()))

        self.assertIn("project_sla.report_year", data_py[0].keys())
        self.assertIn("project_sla.total_projects", data_py[0].keys())

    @requests_mock.Mocker()
    def test_default_no_data(self, mock: requests_mock.Mocker):
        """Test fetch default behaviour with no data"""

        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': MOCK_DATASET_RESPONSE},
            {'status_code': 200, 'text': ''}
        ])

        data_py = self.client.fetch(str(uuid4()))

        self.assertIsNone(data_py)

    @requests_mock.Mocker()
    def test_chartjs(self, mock: requests_mock.Mocker):
        """Test fetch to Chart.js specification"""

        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': MOCK_DATASET_RESPONSE},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        visualisation = json.loads(MOCK_DATASET_RESPONSE['visualisation'])
        metadata = json.loads(MOCK_DATASET_RESPONSE['metadata'])

        # check the chart type is resolved
        self.assertEqual(chartjs_spec['chart_type'],
                         visualisation['chartjs-chart']['chartType'])

        # check there is a label for every dataset
        for dataset in chartjs_spec['data']['datasets']:
            self.assertEqual(len(chartjs_spec['data']['labels']),
                             len(dataset['data']))

        mock_dataset_data_response = json.loads(MOCK_DATASET_DATA_RESPONSE)

        # check the metadata columns are parsed as labels
        for col in metadata['related_table']['columns']:
            key = f"{metadata['name']}.{col['name']}"
            data = [data[key] for data in mock_dataset_data_response]
            self.assertEqual(chartjs_spec['data']['labels'], [
                             str(d) for d in data])

        # check the metadata aggregates are parsed as data
        for col in metadata['related_table']['aggregates']:
            key = f"{metadata['name']}.{col['name']}"
            data = [data[key] for data in mock_dataset_data_response]

            for dataset in chartjs_spec['data']['datasets']:
                self.assertEqual(dataset['data'], data)

    @requests_mock.Mocker()
    def test_chartjs_to_line_chart_from_area_or_scatter(self, mock: requests_mock.Mocker):
        """
        Test fetch to Chart.js specification returns a line chart type if area or scatter is
        specified in the dataset visualisation
        """

        mock_dataset_response_copy = copy.deepcopy(MOCK_DATASET_RESPONSE)
        visualisation = json.loads(mock_dataset_response_copy['visualisation'])
        visualisation['chartjs-chart']['chartType'] = 'area'
        mock_dataset_response_copy['visualisation'] = json.dumps(visualisation)
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': mock_dataset_response_copy},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertEqual(chartjs_spec['chart_type'], 'line')

        visualisation['chartjs-chart']['chartType'] = 'scatter'
        mock_dataset_response_copy['visualisation'] = json.dumps(visualisation)
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': mock_dataset_response_copy},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertEqual(chartjs_spec['chart_type'], 'line')

    @requests_mock.Mocker()
    def test_chartjs_no_metadata(self, mock: requests_mock.Mocker):
        """Test fetch to Chart.js specification with no metadata"""

        mock_dataset_response_copy = copy.deepcopy(MOCK_DATASET_RESPONSE)
        mock_dataset_response_copy['metadata'] = None
        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': mock_dataset_response_copy},
            {'status_code': 200, 'text': MOCK_DATASET_DATA_RESPONSE}
        ])

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertIsNone(chartjs_spec)

    @requests_mock.Mocker()
    def test_chartjs_no_data(self, mock: requests_mock.Mocker):
        """Test fetch to Chart.js specification with no data"""

        mock.get(requests_mock.ANY, [
            {'status_code': 200, 'json': MOCK_DATASET_RESPONSE},
            {'status_code': 200, 'text': ''}
        ])

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertIsNone(chartjs_spec)
