# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zbase', 'zcommon']

package_data = \
{'': ['*'], 'zbase': ['templates/base/*']}

setup_kwargs = {
    'name': 'zohavi',
    'version': '0.1.3',
    'description': '',
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
