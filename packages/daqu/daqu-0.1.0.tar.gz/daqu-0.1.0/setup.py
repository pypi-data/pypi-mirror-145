# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daqu']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'daqu',
    'version': '0.1.0',
    'description': 'DAta QUality Assessment Framework',
    'long_description': '# DAta QUality Assessment\n\nStatus: PRE-ALPHA\n\nA lightweight data quality assessment framework,\nparticularly dealing with the issues of restatements\n(aka retroactive changes, preliminary data, vintage data)',
    'author': 'Kerstin Frailey',
    'author_email': 'frailey.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
