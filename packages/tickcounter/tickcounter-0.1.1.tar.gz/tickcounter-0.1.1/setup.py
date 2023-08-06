# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tickcounter', 'tickcounter.questionnaire', 'tickcounter.util']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2', 'pandas>=1.3.5', 'scipy>=1.4.1', 'seaborn>=0.11.2']

setup_kwargs = {
    'name': 'tickcounter',
    'version': '0.1.1',
    'description': 'A library for processing questionnaire data',
    'long_description': 'Work in progress',
    'author': 'Ong Eng Kheng',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
