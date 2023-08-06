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
    'version': '0.3.2',
    'description': 'A Python library for working with the RIPE Atlas anchoring mesh.',
    'long_description': '<p align="center">\n  <img src="/docs/logo.png" height="150"><br/>\n  <i>A Python library for working with the RIPE Atlas anchoring mesh.</i><br/><br/>\n  <a href="https://codecov.io/gh/SmartMonitoringSchemes/fetchmesh">\n    <img src="https://img.shields.io/codecov/c/github/SmartMonitoringSchemes/fetchmesh?logo=codecov&logoColor=white">\n  </a>\n  <a href="https://github.com/SmartMonitoringSchemes/fetchmesh/raw/gh-pages/fetchmesh.pdf">\n    <img src="https://img.shields.io/badge/documentation-pdf-blue.svg?logo=readthedocs&logoColor=white&style=flat">\n  </a>\n  <a href="https://pypi.org/project/fetchmesh/">\n    <img src="https://img.shields.io/pypi/v/fetchmesh?color=blue&logo=pypi&logoColor=white">\n  </a>\n  <a href="https://github.com/SmartMonitoringSchemes/fetchmesh/actions">\n    <img src="https://img.shields.io/github/workflow/status/SmartMonitoringSchemes/fetchmesh/CI?logo=github&label=tests">\n  </a>\n</p>\n\nfetchmesh is a tool to simplify working with Atlas [anchoring mesh](https://atlas.ripe.net/about/anchors/) measurements. It can download results concurrently, process large files in streaming without requiring a large amount of memory, and clean measurement results. It uses Facebook [Zstandard](https://facebook.github.io/zstd/) algorithm for fast data compression.\n\n- [**Documentation**](https://github.com/SmartMonitoringSchemes/fetchmesh/raw/gh-pages/fetchmesh.pdf) — Consult the quick start guide and the documentation.\n- [**Issues**](https://github.com/SmartMonitoringSchemes/fetchmesh/issues) — See what is broken / currently not working.\n\n## :rocket: Quick Start\n\n```bash\n# Requires Python 3.7+\npip install fetchmesh\n```\n\n```bash\nfetchmesh --help\n# Usage: fetchmesh [OPTIONS] COMMAND [ARGS]...\n# ...\n```\n\nSee the [documentation](https://github.com/SmartMonitoringSchemes/fetchmesh/raw/gh-pages/fetchmesh.pdf) for more.\n\n*Logo: Pizza by Denis Shumaylov from the Noun Project (Creative Commons).*\n',
    'author': 'Maxime Mouchet',
    'author_email': 'max@maxmouchet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SmartMonitoringSchemes/fetchmesh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
