# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pca', 'pca.errors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pca-errors',
    'version': '0.1.0',
    'description': 'Declarative, parametrizable & l10n-independent errors for python-clean-architecture.',
    'long_description': '',
    'author': 'lhaze',
    'author_email': 'github@lhaze.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pcah/pca-errors',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
