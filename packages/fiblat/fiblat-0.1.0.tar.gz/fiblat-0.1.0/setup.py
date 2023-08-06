# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fiblat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fiblat',
    'version': '0.1.0',
    'description': 'A package for generating evenly distributed points on a sphere',
    'long_description': None,
    'author': 'Erik Brinkman',
    'author_email': 'erik.brinkman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erikbrinkman/fibonacci_lattice',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
