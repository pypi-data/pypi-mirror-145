# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postal_address', 'postal_address.tests']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=13,<14', 'boltons>=21,<22', 'pycountry==22.3.5']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0,<3.0']}

setup_kwargs = {
    'name': 'postal-address',
    'version': '22.4.1',
    'description': 'Parse, normalize and render postal addresses.',
    'long_description': None,
    'author': 'Scaleway',
    'author_email': 'opensource@scaleway.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Scaleway/postal-address',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
