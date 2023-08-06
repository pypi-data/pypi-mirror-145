# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gradient_metrics']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'torch>=1.4.0']

setup_kwargs = {
    'name': 'gradient-metrics',
    'version': '0.1.7',
    'description': 'Neural Network Gradient Metrics with PyTorch',
    'long_description': '<div align="center">\n\n[![PyPI](https://img.shields.io/pypi/v/gradient-metrics)](https://pypi.org/project/gradient-metrics/) ![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/ronmckay/gradient_metrics/Publish%20to%20PyPI/main) [![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) [![PyPI - License](https://img.shields.io/pypi/l/gradient-metrics)](LICENSE) ![PyPI - Downloads](https://img.shields.io/pypi/dm/gradient-metrics)\n\n</div>\n\n# Installation\n\n```python\npip install gradient-metrics\n```\n\nThis package implements utilities for computing gradient metrics for measuring uncertainties in neural networks based on the paper "[Classification Uncertainty of Deep Neural Networks Based on Gradient Information](https://arxiv.org/abs/1805.08440)".\n\nDocumentation and examples can be found on [GitHub pages](https://ronmckay.github.io/gradient_metrics/).\n\n# Citing\n\n@inproceedings{OberdiekRG18,  \n  author    = {Philipp Oberdiek and  \n               Matthias Rottmann and  \n               Hanno Gottschalk},  \n  editor    = {Luca Pancioni and  \n               Friedhelm Schwenker and  \n               Edmondo Trentin},  \n  title     = {Classification Uncertainty of Deep Neural Networks Based on Gradient  \n               Information},  \n  booktitle = {Artificial Neural Networks in Pattern Recognition - 8th {IAPR} {TC3}  \n               Workshop, {ANNPR} 2018, Siena, Italy, September 19-21, 2018, Proceedings},  \n  series    = {Lecture Notes in Computer Science},  \n  volume    = {11081},  \n  pages     = {113--125},  \n  publisher = {Springer},  \n  year      = {2018},  \n  url       = { https://doi.org/10.1007/978-3-319-99978-4_9 },  \n  doi       = { 10.1007/978-3-319-99978-4\\_9 },  \n}',
    'author': 'Philipp Oberdiek',
    'author_email': 'git@oberdiek.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RonMcKay/gradient_metrics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
