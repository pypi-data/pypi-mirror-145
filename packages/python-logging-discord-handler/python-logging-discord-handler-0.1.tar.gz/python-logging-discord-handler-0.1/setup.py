# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_logging']

package_data = \
{'': ['*']}

install_requires = \
['discord-webhook>=0.15.0,<0.16.0']

extras_require = \
{'docs': ['Sphinx>=4.4.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinx-sitemap>=2.2.0,<3.0.0',
          'sphinx-autodoc-typehints[docs]>=1.16.0,<2.0.0']}

setup_kwargs = {
    'name': 'python-logging-discord-handler',
    'version': '0.1',
    'description': 'Direct Python log output to Discord',
    'long_description': None,
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@opensourcehacker.com',
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
