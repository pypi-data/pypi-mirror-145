# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spicypy']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3,<4',
 'lpsd>=0.2,<0.3',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.18,<2.0',
 'scipy>=1.5,<2.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=1.1.3,<2.0.0']}

setup_kwargs = {
    'name': 'spicypy',
    'version': '0.1.0',
    'description': 'A python package for signal processing & control systems. Combining several tools to facilitate signal processing, control systems modelling, and the interface between the two.',
    'long_description': None,
    'author': 'Artem Basalaev',
    'author_email': 'artem.basalaev@physikDOTuni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pyda-group/spicypy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
