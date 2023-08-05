# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cellfree']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'cellfree',
    'version': '0.0.1',
    'description': 'A cell free DNA analysis suite',
    'long_description': '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Github Actions](https://github.com/zztin/cellfree/actions/workflows/python-check.yaml/badge.svg)](https://github.com/zztin/cellfree/wayback-machine-saver/actions/workflows/python-check.yaml)\n\n[![PyPI Package latest release](https://img.shields.io/pypi/v/cellfree.svg?style=flat-square)](https://pypi.org/project/cellfree/)\n[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/cellfree?style=flat-square)](https://pypi.org/project/cellfree/)\n[![Supported versions](https://img.shields.io/pypi/pyversions/cellfree.svg?style=flat-square)](https://pypi.org/project/cellfree/)\n\n\n# cellfree\n\nA cell free DNA analysis suite\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n\n## Usage\n\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nLiting Chen <litingchen16@gmail.com>\n\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/1.1.2) version 1.1.2\n',
    'author': 'Liting Chen',
    'author_email': 'litingchen16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zztin/cellfree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
