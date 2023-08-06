# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt_junitxml']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1', 'junit-xml>=1.9']

entry_points = \
{'console_scripts': ['dbt-junitxml = dbt_junitxml.main:cli']}

setup_kwargs = {
    'name': 'dbt-junitxml',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Charles Lariviere',
    'author_email': 'charleslariviere1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chasleslr/dbt-junitxml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
