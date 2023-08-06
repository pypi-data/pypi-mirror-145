# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['davxmppsync']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'xmpppy>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dav-xmpp-sync = davxmppsync.__main__:main']}

setup_kwargs = {
    'name': 'dav-xmpp-sync',
    'version': '1.0.0',
    'description': 'Synchronizes contact names from CardDav to XMPP/SMS gateways',
    'long_description': None,
    'author': 'Sumit Khanna',
    'author_email': 'sumit@penguindreams.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
