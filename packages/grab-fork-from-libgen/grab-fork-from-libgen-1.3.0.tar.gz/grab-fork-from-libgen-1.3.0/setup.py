# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grab_fork_from_libgen']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'lxml>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'grab-fork-from-libgen',
    'version': '1.3.0',
    'description': 'A fork from grab-convert-from-libgen',
    'long_description': None,
    'author': 'Lamarcke',
    'author_email': 'cassiolamarcksilvafreitas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
