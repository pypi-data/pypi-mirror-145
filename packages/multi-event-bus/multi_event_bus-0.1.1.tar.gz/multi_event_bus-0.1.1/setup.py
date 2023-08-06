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
    'version': '0.1.1',
    'description': 'event bus implementation in python with sync and async support',
    'long_description': '# event-bus\n[![Run Tests](https://github.com/hvuhsg/event-bus/actions/workflows/test.yml/badge.svg)](https://github.com/hvuhsg/event-bus/actions/workflows/test.yml)  \nEventBus implementation in python\n\n\n### Examples\n#### sync\n\n```python\nfrom multi_event_bus import EventBus, Consumer\n\neb = EventBus()\nconsumer = Consumer(eb)\n\neb.dispatch("event-name", payload={"num": 1})\n\nconsumer.subscribe_to("event-name")\n\nevent = consumer.get()  # Blocking\n\nprint(event.payload)  # -> {"num": 1}\n```\n#### async\n\n```python\nfrom multi_event_bus import AsyncEventBus, AsyncConsumer\n\neb = AsyncEventBus()\nconsumer = AsyncConsumer(eb)\n\neb.dispatch("event-name", payload={"num": 1})\n\nconsumer.subscribe_to("event-name")\n\nevent = await consumer.get()\n\nprint(event.payload)  # -> {"num": 1}\n```\n#### register event schema\n\n```python\nfrom multi_event_bus import EventBus, Consumer\n\neb = EventBus()\nconsumer = Consumer(eb)\n\n# Enforce json schema of event\njson_schema = {\n    "type": "object",\n    "properties": {"num": {"type": "string"}}\n}\neb.register_event_schema("event-name", schema=json_schema)\n\neb.dispatch("event-name", payload={"num": "7854"})\n\nconsumer.subscribe_to("event-name")\n\nevent = consumer.get()  # Blocking\n\nprint(event.payload)  # -> {"num": "7854"}\n```\n\n### Development\n#### scripts\n```commandline\npoetry run run_pytest\npoetry run run_flake8\npoetry run run_mypy\npoetry run run_black\n```\n#### run tests\n```commandline\npoetry run test\n```\n\n#### run all (test and black)\n```commandline\npoetry run all\n```\n',
    'author': 'yehoyada',
    'author_email': 'hvuhsg5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hvuhsg/event-bus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
