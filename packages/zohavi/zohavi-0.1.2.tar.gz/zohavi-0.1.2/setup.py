# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zbase', 'zcommon']

package_data = \
{'': ['*'], 'zbase': ['templates/base/*']}

install_requires = \
['Flask-Classful>=0.14.2,<0.15.0',
 'Flask-Login>=0.6.0,<0.7.0',
 'Flask>=2.0.0,<3.0.0',
 'pytz>=2022.1,<2023.0']

setup_kwargs = {
    'name': 'zohavi',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
