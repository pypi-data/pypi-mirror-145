# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlraw']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0', 'psycopg2>=2.9.3,<3.0.0', 'redis>=4.2.2,<5.0.0']

setup_kwargs = {
    'name': 'sqlraw',
    'version': '0.1.1',
    'description': 'Path base SQL Query',
    'long_description': None,
    'author': 'Uygun Bodur',
    'author_email': 'uygun@dop.com.tr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/developerkitchentr/sqlraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
