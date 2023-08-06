# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_poetrino']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'test-poetrino',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sasen Perera',
    'author_email': 'sasen.learnings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
