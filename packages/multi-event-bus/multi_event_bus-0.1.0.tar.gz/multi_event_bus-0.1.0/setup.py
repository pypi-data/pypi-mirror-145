# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multi_event_bus']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema']

entry_points = \
{'console_scripts': ['all = scripts.poetry_scripts:run_all',
                     'run_black = scripts.poetry_scripts:run_black',
                     'run_flake8 = scripts.poetry_scripts:run_flake8',
                     'run_mypy = scripts.poetry_scripts:run_mypy',
                     'run_pytest = scripts.poetry_scripts:run_pytest',
                     'test = scripts.poetry_scripts:run_all_tests']}

setup_kwargs = {
    'name': 'multi-event-bus',
    'version': '0.1.0',
    'description': 'event bus implementation in python with sync and async support',
    'long_description': None,
    'author': 'yehoyada',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
