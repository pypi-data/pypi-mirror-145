# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiotrap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tiotrap',
    'version': '0.2',
    'description': 'Helper For Capturing Text IO Streams like stdout, stderr',
    'long_description': None,
    'author': 'Timothy C. Quinn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
