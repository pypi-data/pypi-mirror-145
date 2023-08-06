# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdata_stream_parser',
 'sfdata_stream_parser.filters',
 'sfdata_stream_parser.parser']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.12.0,<9.0.0']

extras_require = \
{'openpyxl': ['openpyxl>=3.0.9,<4.0.0']}

setup_kwargs = {
    'name': 'sfdata-stream-parser',
    'version': '0.4.0',
    'description': 'Loosely inspired by the Streaming API for XML (StAX), this library provides a Python iterator interface for working with tabular documents.',
    'long_description': None,
    'author': 'Kaj Siebert',
    'author_email': 'kaj@k-si.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
