# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dccmd',
 'dccmd.main',
 'dccmd.main.auth',
 'dccmd.main.crypto',
 'dccmd.main.models',
 'dccmd.main.upload',
 'dccmd.main.util']

package_data = \
{'': ['*']}

install_requires = \
['SecretStorage>=3.3.1,<4.0.0',
 'dracoon>=1.3.1,<2.0.0',
 'keyring>=23.5.0,<24.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['dccmd = dccmd:app']}

setup_kwargs = {
    'name': 'dccmd',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Octavio Simone',
    'author_email': '70800577+unbekanntes-pferd@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
