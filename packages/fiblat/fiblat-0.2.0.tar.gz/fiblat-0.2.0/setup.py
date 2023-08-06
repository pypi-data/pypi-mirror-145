# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fiblat']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.55.1,<0.56.0']

setup_kwargs = {
    'name': 'fiblat',
    'version': '0.2.0',
    'description': 'A package for generating evenly distributed points on a sphere',
    'long_description': None,
    'author': 'Erik Brinkman',
    'author_email': 'erik.brinkman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erikbrinkman/fibonacci_lattice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
