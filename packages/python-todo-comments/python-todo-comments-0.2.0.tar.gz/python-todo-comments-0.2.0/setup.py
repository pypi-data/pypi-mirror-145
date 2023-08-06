# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_todo_comments']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['py-todos = python_todo_comments.main:main']}

setup_kwargs = {
    'name': 'python-todo-comments',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Tylor Dodge',
    'author_email': 'tdodge@nexamp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
