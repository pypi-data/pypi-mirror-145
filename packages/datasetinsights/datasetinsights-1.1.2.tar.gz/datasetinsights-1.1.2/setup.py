# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasetinsights',
 'datasetinsights.commands',
 'datasetinsights.datasets',
 'datasetinsights.datasets.transformers',
 'datasetinsights.datasets.unity_perception',
 'datasetinsights.io',
 'datasetinsights.io.downloader',
 'datasetinsights.stats',
 'datasetinsights.stats.image_analysis',
 'datasetinsights.stats.visualization']

package_data = \
{'': ['*'], 'datasetinsights.stats.visualization': ['font/*']}

install_requires = \
['click==8.0.4',
 'codetiming>=1.2.0,<2.0.0',
 'cython>=0.29.14,<0.30.0',
 'dash>=2.3.1,<3.0.0',
 'dask[complete]>=2.14.0,<3.0.0',
 'google-cloud-storage>=1.24.1,<2.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'numpy>=1.17,<2.0',
 'opencv-python>=4.4.0.42,<5.0.0.0',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=5.0.0',
 'pyquaternion>=0.9.5,<0.10.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['datasetinsights = datasetinsights.__main__:entrypoint']}

setup_kwargs = {
    'name': 'datasetinsights',
    'version': '1.1.2',
    'description': 'Synthetic dataset insights.',
    'long_description': '# Dataset Insights\n\n[![PyPI python](https://img.shields.io/pypi/pyversions/datasetinsights)](https://pypi.org/project/datasetinsights)\n[![PyPI version](https://badge.fury.io/py/datasetinsights.svg)](https://pypi.org/project/datasetinsights)\n[![Downloads](https://pepy.tech/badge/datasetinsights)](https://pepy.tech/project/datasetinsights)\n[![Tests](https://github.com/Unity-Technologies/datasetinsights/actions/workflows/linting-and-unittests.yaml/badge.svg?branch=master&event=push)](https://github.com/Unity-Technologies/datasetinsights/actions/workflows/linting-and-unittests.yaml?query=branch%3Amaster+event%3Apush)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)\n\nUnity Dataset Insights is a python package for downloading, parsing and analyzing synthetic datasets generated using the Unity [Perception package](https://github.com/Unity-Technologies/com.unity.perception).\n\n## Installation\n\nDatasetinsights is published to PyPI. You can simply run `pip install datasetinsights` command under a supported python environments:\n\n## Getting Started\n\n### Dataset Statistics\n\nWe provide a sample [notebook](notebooks/Perception_Statistics.ipynb) to help you load synthetic datasets generated using [Perception package](https://github.com/Unity-Technologies/com.unity.perception) and visualize dataset statistics. We plan to support other sample Unity projects in the future.\n\n### Load Datasets\n\nThe [Unity Perception](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.datasets.unity_perception.html#datasetinsights-datasets-unity-perception) package provides datasets under this [schema](https://datasetinsights.readthedocs.io/en/latest/Synthetic_Dataset_Schema.html#synthetic-dataset-schema). The datasetinsighs package also provide convenient python modules to parse datasets.\n\nFor example, you can load `AnnotationDefinitions` into a python dictionary by providing the corresponding annotation definition ID:\n\n```python\nfrom datasetinsights.datasets.unity_perception import AnnotationDefinitions\n\nannotation_def = AnnotationDefinitions(data_root=dest, version="my_schema_version")\ndefinition_dict = annotation_def.get_definition(def_id="my_definition_id")\n```\n\nSimilarly, for `MetricDefinitions`:\n```python\nfrom datasetinsights.datasets.unity_perception import MetricDefinitions\n\nmetric_def = MetricDefinitions(data_root=dest, version="my_schema_version")\ndefinition_dict = metric_def.get_definition(def_id="my_definition_id")\n```\n\nThe `Captures` table provide the collection of simulation captures and annotations. You can load these records directly as a Pandas `DataFrame`:\n\n```python\nfrom datasetinsights.datasets.unity_perception import Captures\n\ncaptures = Captures(data_root=dest, version="my_schema_version")\ncaptures_df = captures.filter(def_id="my_definition_id")\n```\n\n\nThe `Metrics` table can store simulation metrics for a capture or annotation. You can also load these records as a Pandas `DataFrame`:\n\n```python\nfrom datasetinsights.datasets.unity_perception import Metrics\n\nmetrics = Metrics(data_root=dest, version="my_schema_version")\nmetrics_df = metrics.filter_metrics(def_id="my_definition_id")\n```\n\n### Download Datasets\n\nYou can download the datasets using the [download](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.commands.html#datasetinsights-commands-download) command:\n\n```bash\ndatasetinsights download --source-uri=<xxx> --output=$HOME/data\n```\n\nThe download command supports HTTP(s), and GCS.\n\nAlternatively, you can download dataset directly from python [interface](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.io.downloader.html#module-datasetinsights.io.downloader).\n\n`GCSDatasetDownloader` can download a dataset from GCS locations.\n```python\nfrom datasetinsights.io.downloader import GCSDatasetDownloader\n\nsource_uri=gs://url/to/file.zip # or gs://url/to/folder\ndest = "~/data"\ndownloader = GCSDatasetDownloader()\ndownloader.download(source_uri=source_uri, output=dest)\n```\n\n`HTTPDatasetDownloader` can a dataset from any HTTP(S) url.\n```python\nfrom datasetinsights.io.downloader import HTTPDatasetDownloader\n\nsource_uri=http://url.to.file.zip\ndest = "~/data"\ndownloader = HTTPDatasetDownloader()\ndownloader.download(source_uri=source_uri, output=dest)\n```\n\n### Convert Datasets\n\nIf you are interested in converting the synthetic dataset to COCO format for\nannotations that COCO supports, you can run the `convert` command:\n\n```bash\ndatasetinsights convert -i <input-directory> -o <output-directory> -f COCO-Instances\n```\nor\n```bash\ndatasetinsights convert -i <input-directory> -o <output-directory> -f COCO-Keypoints\n```\n\nYou will need to provide 2D bounding box definition ID in the synthetic dataset. We currently only support 2D bounding box and human keypoint annotations for COCO format.\n\n## Docker\n\nYou can use the pre-build docker image [unitytechnologies/datasetinsights](https://hub.docker.com/r/unitytechnologies/datasetinsights) to interact with datasets.\n\n## Documentation\n\nYou can find the API documentation on [readthedocs](https://datasetinsights.readthedocs.io/en/latest/).\n\n## Contributing\n\nPlease let us know if you encounter a bug by filing an issue. To learn more about making a contribution to Dataset Insights, please see our Contribution [page](CONTRIBUTING.md).\n\n## License\n\nDataset Insights is licensed under the Apache License, Version 2.0. See [LICENSE](LICENCE) for the full license text.\n\n## Citation\nIf you find this package useful, consider citing it using:\n```\n@misc{datasetinsights2020,\n    title={Unity {D}ataset {I}nsights Package},\n    author={{Unity Technologies}},\n    howpublished={\\url{https://github.com/Unity-Technologies/datasetinsights}},\n    year={2020}\n}\n```\n',
    'author': 'Unity AI Perception Team',
    'author_email': 'computer-vision@unity3d.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unity-Technologies/datasetinsights',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
