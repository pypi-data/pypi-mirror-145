# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tree_router']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'djangorestframework>=3.7.0']

setup_kwargs = {
    'name': 'drf-tree-router',
    'version': '0.1.1',
    'description': 'Create browsable routes by nesting routers in a tree-like structure.',
    'long_description': '# Django REST Framework Tree Router\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Python Version][version-badge]][pypi]\n\n```shell\npip install drf-tree-router\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/drf-tree-router/](https://mrthearman.github.io/drf-tree-router/)\n\n**Source Code**: [https://github.com/MrThearMan/drf-tree-router/](https://github.com/MrThearMan/drf-tree-router/)\n\n---\n\nA Django REST Framework router that can be nested with other routers to create a tree-like structure\nof your API endpoints. The router also accepts APIViews in addition to ViewSets.\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/drf-tree-router/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/drf-tree-router/Tests\n[pypi-badge]: https://img.shields.io/pypi/v/drf-tree-router\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/drf-tree-router\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/drf-tree-router\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/drf-tree-router\n[version-badge]: https://img.shields.io/pypi/pyversions/drf-tree-router\n\n[coverage]: https://coveralls.io/github/MrThearMan/drf-tree-router?branch=main\n[status]: https://github.com/MrThearMan/drf-tree-router/actions/workflows/main.yml\n[pypi]: https://pypi.org/project/drf-tree-router\n[licence]: https://github.com/MrThearMan/drf-tree-router/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/drf-tree-router/commits/main\n[issues]: https://github.com/MrThearMan/drf-tree-router/issues\n',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrThearMan/drf-tree-router',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
