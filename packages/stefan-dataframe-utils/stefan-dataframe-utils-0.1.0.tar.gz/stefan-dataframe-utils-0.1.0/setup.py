# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\main\\python'}

packages = \
['stefan_dataframe_utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.1.5', 'pyarrow==6.0.1', 'python-json-logger>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'stefan-dataframe-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefan Bader',
    'author_email': 'baderstefan@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.7.0',
}


setup(**setup_kwargs)
