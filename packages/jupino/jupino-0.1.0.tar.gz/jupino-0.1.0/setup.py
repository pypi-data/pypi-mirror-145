# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupino', 'jupino.widgets']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'jupino',
    'version': '0.1.0',
    'description': 'Annotate data using Jupyter notebook',
    'long_description': None,
    'author': 'Sanjaya Subedi',
    'author_email': 'jangedoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
