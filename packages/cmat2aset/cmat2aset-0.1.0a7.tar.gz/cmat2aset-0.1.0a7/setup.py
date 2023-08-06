# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmat2aset']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'cmat2aset',
    'version': '0.1.0a7',
    'description': 'correlation matrix to align set ',
    'long_description': '# cmat2aset\n[![pytest](https://github.com/ffreemt/cmat2aset/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/cmat2aset/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/cmat2aset.svg)](https://badge.fury.io/py/cmat2aset)\n\ncmat2aset descr\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/cmat2aset\n# poetry add git+https://github.com/ffreemt/cmat2aset\n# git clone https://github.com/ffreemt/cmat2aset && cd cmat2aset\n```\n\n## Use it\n```python\nfrom cmat2aset import cmat2aset\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/cmat2aset',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0',
}


setup(**setup_kwargs)
