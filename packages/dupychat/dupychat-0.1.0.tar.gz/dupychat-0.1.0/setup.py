# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dupychat',
 'dupychat.config',
 'dupychat.core',
 'dupychat.core_async',
 'dupychat.core_multithread',
 'dupychat.paramgen',
 'dupychat.parser',
 'dupychat.processors',
 'dupychat.processors.compatible',
 'dupychat.processors.compatible.renderer',
 'dupychat.processors.default',
 'dupychat.processors.default.renderer',
 'dupychat.processors.speed',
 'dupychat.processors.superchat',
 'dupychat.util']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'dupychat',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dunossauro',
    'author_email': 'mendesxeduardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
