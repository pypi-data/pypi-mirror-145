# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hugedict', 'hugedict.parallel']

package_data = \
{'': ['*']}

install_requires = \
['lbry-rocksdb-optimized>=0.8.1,<0.9.0',
 'pybloomfiltermmap3>=0.5.5,<0.6.0',
 'zstandard>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'hugedict',
    'version': '1.2.1',
    'description': 'A dictionary-like object that is friendly with multiprocessing and uses key-value databases (e.g., RocksDB) as the underlying storage.',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binh-vu/hugedict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
