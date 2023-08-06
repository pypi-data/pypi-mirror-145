# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['evento']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'evento',
    'version': '2.0.0',
    'description': 'Observer pattern made muy facil',
    'long_description': None,
    'author': 'Mark van de Korput',
    'author_email': 'dr.theman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
