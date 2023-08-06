# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mecab2pandas', 'mecab2pandas.exception']

package_data = \
{'': ['*']}

install_requires = \
['mecab-python3', 'pandas', 'unidic-lite']

setup_kwargs = {
    'name': 'mecab2pandas',
    'version': '0.2.3',
    'description': 'MeCab to pandas',
    'long_description': None,
    'author': 'Lucky',
    'author_email': 'phatbowie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lucky-Mano/mecab2pandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
