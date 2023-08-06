# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapper']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'docstring-parser>=0.13,<0.14',
 'dominate>=2.6.0,<3.0.0',
 'python-slugify>=6.1.1,<7.0.0']

setup_kwargs = {
    'name': 'yapper',
    'version': '0.2.0b1',
    'description': 'Simple python parser converting docstrings to .astro files for the Astro static site generator.',
    'long_description': None,
    'author': 'Gareth Simons',
    'author_email': 'garethsimons@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
