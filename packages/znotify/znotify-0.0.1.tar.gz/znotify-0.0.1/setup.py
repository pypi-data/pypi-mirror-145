# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['znotify']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'znotify',
    'version': '0.0.1',
    'description': 'sdk for notify',
    'long_description': None,
    'author': 'Zxilly',
    'author_email': 'zhouxinyu1001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
