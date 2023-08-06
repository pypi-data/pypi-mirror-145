# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devind_dictionaries',
 'devind_dictionaries.migrations',
 'devind_dictionaries.models',
 'devind_dictionaries.schema',
 'devind_dictionaries.tasks',
 'devind_dictionaries.tests']

package_data = \
{'': ['*'], 'devind_dictionaries.tests': ['data/*']}

install_requires = \
['Django>=3.2.12,<5.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'celery>=5.2.5,<6.0.0',
 'devind-helpers>=0,<1',
 'graphene-django-filter>=0.6.4,<0.7.0',
 'graphene-django>=2.15.0,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'devind-dictionaries',
    'version': '0.2.2',
    'description': 'Common dictionaries for devind applications.',
    'long_description': '# Devind project template\n\n[![CI](https://github.com/devind-team/devind-django-dictionaries/workflows/Release/badge.svg)](https://github.com/devind-team/devind-django-dictionaries/actions)\n[![Coverage Status](https://coveralls.io/repos/github/devind-team/devind-django-dictionaries/badge.svg?branch=main)](https://coveralls.io/github/devind-team/devind-django-dictionaries?branch=main)\n[![PyPI version](https://badge.fury.io/py/devind-dictionaries.svg)](https://badge.fury.io/py/devind-dictionaries)\n[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](https://opensource.org/licenses/MIT)\n\n\n# Installation\n```shell\n# pip\npip install devind_dictionaries\n# poetry\npoetry add devind_dictionaries\n```',
    'author': 'Luferov Victor',
    'author_email': 'lyferov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/devind-django-dictionaries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
