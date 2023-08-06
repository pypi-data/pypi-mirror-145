# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_scores']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1.7,<3.0.0',
 'fastlid>=0.1.7,<0.2.0',
 'joblib>=1.0.1,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'msgpack>=1.0.2,<2.0.0',
 'nltk>=3.6.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'simplemma>=0.3.0,<0.4.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'fast-scores',
    'version': '0.1.3a3',
    'description': ' ',
    'long_description': '# fast-scores\n[![tests](https://github.com/ffreemt/fast-scores/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fast_scores.svg)](https://badge.fury.io/py/fast_scores)\n\nCalculate correlatioin matrix fast\n\n## Usage\n\n```shell\n\n```',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/fast-scores',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
