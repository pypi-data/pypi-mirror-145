# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymine_server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymine-server',
    'version': '0.0.0',
    'description': 'A fast and easy to use, moddable, Python based Minecraft server!',
    'long_description': None,
    'author': 'Milo Weinberg',
    'author_email': 'iapetus011@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
