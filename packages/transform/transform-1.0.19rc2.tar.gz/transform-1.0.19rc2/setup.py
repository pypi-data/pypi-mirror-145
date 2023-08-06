# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transform',
 'transform.cli',
 'transform.vendor.gql',
 'transform.vendor.gql.transport',
 'transform.vendor.gql.utilities',
 'transform.vendor.graphql3',
 'transform.vendor.graphql3.error',
 'transform.vendor.graphql3.execution',
 'transform.vendor.graphql3.language',
 'transform.vendor.graphql3.pyutils',
 'transform.vendor.graphql3.subscription',
 'transform.vendor.graphql3.type',
 'transform.vendor.graphql3.utilities',
 'transform.vendor.graphql3.validation',
 'transform.vendor.graphql3.validation.rules',
 'transform.vendor.graphql3.validation.rules.custom',
 'transform.vendor.idna',
 'transform.vendor.multidict',
 'transform.vendor.yarl']

package_data = \
{'': ['*'],
 'transform': ['vendor/graphql_core-3.2.0.dist-info/*',
               'vendor/idna-3.3.dist-info/*',
               'vendor/multidict-6.0.2.dist-info/*',
               'vendor/yarl-1.7.2.dist-info/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=1.2.2,<2.0.0',
 'click==7.1.2',
 'log-symbols>=0.0.14,<0.0.15',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'transform-tools>=1.0.2,<2.0.0',
 'update-checker>=0.18.0,<0.19.0']

entry_points = \
{'console_scripts': ['mql = transform.cli.mql_cli:cli']}

setup_kwargs = {
    'name': 'transform',
    'version': '1.0.19rc2',
    'description': 'Transform MQL Client Library',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
