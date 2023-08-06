# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['felucca']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.4',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.0.1,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['felucca = felucca.main:app']}

setup_kwargs = {
    'name': 'felucca',
    'version': '0.0.10',
    'description': 'Cairo dependency management and packaging made easy.',
    'long_description': '# Felucca: Dependency Management for Cairo\n\nFelucca helps you declare, manage and install dependencies of Cairo projects, ensuring you have the right stack everywhere.\n\n',
    'author': 'Fran Algaba',
    'author_email': 'f.algaba.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.11,<4.0.0',
}


setup(**setup_kwargs)
