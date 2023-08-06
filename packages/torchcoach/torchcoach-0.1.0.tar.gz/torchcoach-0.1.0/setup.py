# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torchcoach', 'torchcoach.loggers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aiohttp_cors>=0.7.0,<0.8.0',
 'black>=22.3.0,<23.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'prettytable>=3.2.0,<4.0.0',
 'tensorboard>=2.8.0,<3.0.0',
 'torch>=1.11.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'torchcoach',
    'version': '0.1.0',
    'description': 'A project aiming at simplifying training of PyTorch models and provide support for the continual learning setting.',
    'long_description': None,
    'author': 'Reza Davari',
    'author_email': 'rezazzr@hotmail.com',
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
