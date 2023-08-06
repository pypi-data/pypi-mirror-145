# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbox', 'mbox.requests']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

extras_require = \
{'click': ['click>=8.1.2,<9.0.0', 'dateparser>=1.1.1,<2.0.0'],
 'requests': ['requests>=2.27.1,<3.0.0']}

setup_kwargs = {
    'name': 'mbox',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Maxime Mouchet',
    'author_email': 'max@maxmouchet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
