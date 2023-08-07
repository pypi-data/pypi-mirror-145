# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['systemadmin']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.2.0,<6.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'systemadmin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yassine',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
