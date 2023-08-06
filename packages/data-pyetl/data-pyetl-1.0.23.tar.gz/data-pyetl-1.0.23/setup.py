# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_pyetl']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'SQLAlchemy>=1.4.32,<2.0.0',
 'cx-Oracle>=8.3.0,<9.0.0',
 'fdb>=2.0.2,<3.0.0',
 'flake8>=4.0.1,<5.0.0',
 'ipython>=8.1.1,<9.0.0',
 'lxml>=4.8.0,<5.0.0',
 'numpy>=1.22.3,<2.0.0',
 'odfpy>=1.4.1,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyodbc>=4.0.32,<5.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytz>=2021.3,<2022.0',
 'requests-mock>=1.9.3,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'urllib3>=1.26.9,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'data-pyetl',
    'version': '1.0.23',
    'description': 'Data Pyetl is an python approach to extract and load data from a source to a database',
    'long_description': None,
    'author': 'MacSoares',
    'author_email': 'macario.junior@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
