# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetchmesh',
 'fetchmesh.alias',
 'fetchmesh.atlas',
 'fetchmesh.bgp',
 'fetchmesh.commands',
 'fetchmesh.filters',
 'fetchmesh.mocks',
 'fetchmesh.peeringdb',
 'fetchmesh.transformers']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'cached-property>=1.5.1,<2.0.0',
 'click>=8.0,<9.0',
 'mbox[click]>=0.1.10,<0.2.0',
 'pandas>=1.0.1,<2.0.0',
 'psutil>=5.7.0,<6.0.0',
 'py-radix>=0.10.0,<0.11.0',
 'pytz>=2021.1,<2022.0',
 'requests>=2.22.0,<3.0.0',
 'rich>=12.0,<13.0',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.46.0,<5.0.0',
 'zstandard>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['fetchmesh = fetchmesh.commands:main']}

setup_kwargs = {
    'name': 'fetchmesh',
    'version': '0.3.1',
    'description': 'A Python library for working with the RIPE Atlas anchoring mesh.',
    'long_description': None,
    'author': 'Maxime Mouchet',
    'author_email': 'max@maxmouchet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
