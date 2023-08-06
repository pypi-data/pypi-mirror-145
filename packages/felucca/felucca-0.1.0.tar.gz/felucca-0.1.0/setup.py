# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['felucca']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.4',
 'cookiecutter>=1.7.3,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['felucca = felucca.main:app']}

setup_kwargs = {
    'name': 'felucca',
    'version': '0.1.0',
    'description': 'Cairo dependency management and packaging made easy.',
    'long_description': "# Felucca: Dependency Management for Cairo\n\n[![Tests and release](https://github.com/franalgaba/felucca/actions/workflows/release.yml/badge.svg)](https://github.com/franalgaba/felucca/actions/workflows/release.yml)\n\nFelucca helps you declare, manage and install dependencies of Cairo projects, ensuring you have the right stack everywhere.\n\n# Installation\n\nIt supports Python 3.7+:\n\n`pip install felucca`\n\n# Introduction\n\n`felucca` is a tool to handle Cairo contracts installation as well as its packaging levaraging Python native capabilities. Felucca uses [Poetry](https://github.com/python-poetry/poetry) under the hood to handle all Python project management using the [standardized](https://peps.python.org/pep-0518/) `pyproject.toml`.\n\n# Why?\n\nCairo contracts development works very closely with Python for project management, dependency installation and testing. Felucca tries to simplify the process of sharing, installing and managing Cairo contracts between differents projects and working in a more natural manner where packages evolve over time and dependant projects doesn't have to upgrade Cairo contracts manually. Using Felucca's approach to leverage Python capabilties in terms of dependency management and project structure gives many advantages:\n\n* Unified project structure across Cairo packages.\n* Rapid adaptation to changes as the ecosystem evolves.\n* Compatibility management between Cairo contracts with different Cairo versions.\n* Effortless installation for quick usage in new packages.\n* Traceability of Cairo packages and releases.\n* Global availability of Cairo packages.\n* Many more...\n\n# Usage\n\nThis tool provides a set of different command to handle all the product lifecycle for dependency and package management. \n\n## Cairo package project structure creation\n\n`felucca new <package_name>`\n\nThis command will create a project structure for Cairo packages from a [template](https://github.com/franalgaba/felucca-package-template) ready to be used for development.\n\n## Cairo package installation\n\n`felucca install felucca-package-example`\n\nThis command will install the Cairo package into the project while checking Cairo compatibility, keeping traceability using the `pyproject.toml` file to save required metadata and installing the Cairo contracts into the project.\n\n## Cairo package uninstall\n\n`felucca uninstall felucca-package-example`\n\nThis command will remove the Cairo package from the project and all the related metadata.\n\n## Cairo package setup\n\n`felucca setup`\n\nIf you want to check if your project is ready to work as a Cairo package this command will check all the needed requirements to do so. If not properly setup it will fix it for you automatically.\n\n",
    'author': 'Fran Algaba',
    'author_email': 'f.algaba.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.11,<3.9',
}


setup(**setup_kwargs)
