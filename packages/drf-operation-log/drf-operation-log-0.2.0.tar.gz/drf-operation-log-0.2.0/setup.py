# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_operation_log', 'drf_operation_log.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0', 'djangorestframework>=3.13.1,<4.0.0']

setup_kwargs = {
    'name': 'drf-operation-log',
    'version': '0.2.0',
    'description': 'Operation log for drf serializers.',
    'long_description': None,
    'author': 'aiden_lu',
    'author_email': 'aiden_lu@wochacha.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anyidea/drf-operation-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
