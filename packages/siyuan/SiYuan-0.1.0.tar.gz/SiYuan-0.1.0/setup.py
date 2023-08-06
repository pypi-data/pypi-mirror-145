# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siyuan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'siyuan',
    'version': '0.1.0',
    'description': 'SiYuan Api Implement',
    'long_description': None,
    'author': 'InEase',
    'author_email': 'InEase28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
