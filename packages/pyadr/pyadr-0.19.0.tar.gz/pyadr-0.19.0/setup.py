# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyadr', 'pyadr.assets', 'pyadr.cli', 'pyadr.git', 'pyadr.git.cli']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0,<1', 'gitpython>=3.1,<4.0', 'loguru>=0,<1', 'python-slugify>=6,<7']

extras_require = \
{':python_version < "3.7"': ['importlib_resources>=5.0.0,<6.0.0'],
 'bdd': ['behave4git>=0,<1', 'PyHamcrest>=2.0,<3.0'],
 'docs': ['sphinx>=4.2,<5.0',
          'sphinx-autodoc-typehints>=1.10,<2.0',
          'sphinx-autobuild>=2021,<2022',
          'sphinx_rtd_theme>=1,<2',
          'm2r>=0,<1'],
 'format': ['isort>=5,<6', 'black'],
 'lint': ['flake8>=4.0,<5.0',
          'flake8-bugbear>=22,<23',
          'pydocstyle>=6.1,<7.0',
          'pylint>=2.3,<3.0',
          'yapf>=0,<1'],
 'repl': ['bpython>=0,<1'],
 'test': ['pytest>=7.1,<8.0',
          'pytest-cov>=3.0,<4.0',
          'pytest-mock>=3.2,<4.0',
          'pytest-html>=3.1,<4.0',
          'pytest-asyncio>=0,<1',
          'PyHamcrest>=2.0,<3.0'],
 'type': ['mypy>=0,<1', 'types-python-slugify>=5,<6']}

entry_points = \
{'console_scripts': ['git-adr = pyadr.git.cli:main', 'pyadr = pyadr.cli:main']}

setup_kwargs = {
    'name': 'pyadr',
    'version': '0.19.0',
    'description': 'CLI to help with an ADR process lifecycle (proposal/approval/rejection/deprecation/superseeding), which used git.',
    'long_description': None,
    'author': 'Emmanuel Sciara',
    'author_email': 'emmanuel.sciara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opinionated-digital-center/pyadr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
