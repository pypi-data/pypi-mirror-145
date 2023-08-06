# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsondbupload']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsondbupload',
    'version': '1.0.0',
    'description': 'Insert records to relational database from json file',
    'long_description': None,
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
