# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synbconvert']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'mkdocs-click>=0.5.0,<0.6.0',
 'mkdocs-material>=8.2.5,<9.0.0',
 'mkdocs>=1.2.3,<2.0.0',
 'mkdocstrings-python>=0.6.6,<0.7.0',
 'mkdocstrings>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['synbconvert = synbconvert.cli:synbconvert']}

setup_kwargs = {
    'name': 'synbconvert',
    'version': '0.1.0',
    'description': 'A simple command line tool to convert Python files to Synapse Notebooks and vice versa.',
    'long_description': '<p align="center"><img width="300" src="https://raw.githubusercontent.com/alpine-data/synbconvert/main/docs/img/logo.png"/></p>\n\n# synbconvert\n\n[![Documentation](https://img.shields.io/badge/Documentation-MkDocs-blue)](https://alpine-data.github.io/synbconvert/)\n[![Python Build](https://github.com/alpine-data/synbconvert/actions/workflows/python-build.yml/badge.svg)](https://github.com/alpine-data/synbconvert/actions/workflows/python-build.yml)\n\n\nAzure Synapse Analytics uses notebooks for data preparation, data visualization, machine learning, and many other tasks. \nHowever, performing proper version control working with these notebooks is a pain. \nMerging long nested JSON documents with git is nearly impossible.\nIf you would like to use Azure Synapse Analytics for large scale projects while compling with the standards of good software engineering, synbconvert may be the tool you are looking for.\nYou will be able to develop code in your favorite IDE and colaborate with your team as usual.\n\n## Features\n\nsynbconvert is a simple command line tool and Python API to convert Python files to Azure Synapse Analytics notebooks and vice versa.\nThe main features of the tool include:\n\n- Lean annotation syntax for Python files\n- Conversion of Python files to Azure Synapse Analytics notebooks based on annotations\n- Conversion of Azure Synapse Analytics notebooks to annotated Python files\n\n## Workflow\n\n<p align="center"><img width="885" src="https://raw.githubusercontent.com/alpine-data/synbconvert/main/docs/img/workflow.png"/></p>\n\n## Installation\n\n### pip\n\nsynbconvert releases are available as source packages and binary wheels. Before you install synbconvert and its dependencies, make sure that your pip, setuptools and wheel are up to date. When using pip it is generally recommended to install packages in a virtual environment to avoid modifying system state. You can install synbconvert with:\n\n```console\n$ pip install synbconvert\n```\n\n<br>\n',
    'author': 'Jan Bieser',
    'author_email': 'janwithb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alpine-data/synbconvert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
