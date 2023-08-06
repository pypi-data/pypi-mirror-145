# pylint: disable=too-many-locals

"""Parse Service"""

# standard
from datetime import datetime
import re
import uuid
import os
import yaml
# external
from nbconvert import MarkdownExporter
from traitlets.config import Config
# local
from matatika.dataset import Dataset


def parse_yaml(dataset_file, dataset_alias, file_ext):
    """Yaml file parsing"""
    datasets = []
    with open(dataset_file, 'r', encoding='utf8') as yaml_file:
        yaml_datasets = yaml.safe_load(yaml_file)
        if yaml_datasets.get('version') == "datasets/v0.2":
            _, tail = os.path.split(dataset_file)
            dataset_alias = dataset_alias or tail[:-len(file_ext)]
            yaml_datasets = {dataset_alias: yaml_datasets}
        else:
            yaml_datasets = yaml_datasets['datasets']
    if len(yaml_datasets) > 1 and dataset_alias:
        return None
    for alias in yaml_datasets:
        yaml_datasets[alias].update({'alias': dataset_alias or alias})
        dataset = Dataset.from_dict(yaml_datasets[alias])
        datasets.append(dataset)
    return datasets


def parse_notebook(dataset_file, dataset_alias, file_ext):
    """Notebook file parsing"""
    datasets = []
    config = Config()
    config.TemplateExporter.exclude_output_prompt = True
    config.TemplateExporter.exclude_input = True
    config.TemplateExporter.exclude_input_prompt = True
    config.ExtractOutputPreprocessor.enabled = False
    md_exporter = MarkdownExporter(config=config)
    md_str, _resources = md_exporter.from_file(dataset_file)

    match = re.search(r'#+\s(.+)', md_str)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    default_title = f"Generated Report ({timestamp})"
    dataset_title = match.group(1) if match else default_title
    _, tail = os.path.split(dataset_file)

    dataset_alias = dataset_alias or tail[:-len(file_ext)]

    dataset = Dataset.from_dict({
        'id': str(uuid.uuid4()),
        'title': dataset_title,
        'description': md_str,
        'alias': dataset_alias
    })
    datasets.append(dataset)
    return datasets
