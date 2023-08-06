# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arq_dashboard',
 'arq_dashboard.api',
 'arq_dashboard.api.endpoints',
 'arq_dashboard.core',
 'arq_dashboard.schemas']

package_data = \
{'': ['*'],
 'arq_dashboard': ['frontend/*',
                   'frontend/css/*',
                   'frontend/fonts/*',
                   'frontend/js/*']}

install_requires = \
['aiometer>=0.3.0,<0.4.0',
 'arq>=0.22,<0.23',
 'arrow>=1.2.2,<2.0.0',
 'async-cache>=1.1.1,<2.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'loguru>=0.6.0,<0.7.0',
 'pyhumps>=3.5.3,<4.0.0',
 'uvicorn[standard]>=0.17.6,<0.18.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0']}

setup_kwargs = {
    'name': 'arq-dashboard',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
