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
    'version': '0.1.11',
    'description': 'Personal Python toolbox for quick prototyping.',
    'long_description': '# mbox\n\n[![Coverage][cov-badge]][cov-url]\n[![Tests][ci-badge]][ci-url]\n[![PyPI][pypi-badge]][pypi-url]\n\nPersonal Python toolbox for quick prototyping.  \nCode quality is variable, documentation is lacking, but there should be at-least some tests :-)\n\n[ci-badge]: https://img.shields.io/github/workflow/status/maxmouchet/mbox/CI?logo=github&label=tests\n[ci-url]: https://github.com/maxmouchet/mbox/actions/workflows/ci.yml\n\n[cov-badge]: https://img.shields.io/codecov/c/github/maxmouchet/mbox?logo=codecov&logoColor=white\n[cov-url]: https://codecov.io/gh/maxmouchet/mbox\n\n[pypi-badge]: https://img.shields.io/pypi/v/mbox?color=blue&logo=pypi&logoColor=white\n[pypi-url]: https://pypi.org/project/mbox/\n',
    'author': 'Maxime Mouchet',
    'author_email': 'max@maxmouchet.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmouchet/mbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
