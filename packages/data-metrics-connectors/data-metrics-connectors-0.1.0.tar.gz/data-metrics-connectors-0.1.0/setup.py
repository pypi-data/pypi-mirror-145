# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_metric_connector',
 'data_metric_connector.connectors',
 'data_metric_connector.connectors.mongo',
 'data_metric_connector.connectors.mysql',
 'data_metric_connector.connectors.mysql.meta_sql',
 'data_metric_connector.logger',
 'data_metric_connector.utils']

package_data = \
{'': ['*']}

install_requires = \
['flake8-black>=0.3.2,<0.4.0',
 'mongoengine>=0.24.0,<0.25.0',
 'mysql-connector-python>=8.0.28,<9.0.0']

setup_kwargs = {
    'name': 'data-metrics-connectors',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'AADARSH GAIKWAD',
    'author_email': 'aadarshgaikwad96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
