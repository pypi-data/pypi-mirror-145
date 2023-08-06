# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cachette', 'fastapi_cachette.backends']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'dynamodb': ['aiobotocore[examples,dynamodb]>=2.2.0,<3.0.0'],
 'examples': ['uvicorn[examples]==0.15.0',
              'aiomcache[examples,memcached]>=0.7.0,<0.8.0',
              'aiobotocore[examples,dynamodb]>=2.2.0,<3.0.0',
              'redis[examples,redis]>=4.2.1,<5.0.0'],
 'memcached': ['aiomcache[examples,memcached]>=0.7.0,<0.8.0'],
 'mongodb': ['motor[examples,mongodb]>=2.5.1,<3.0.0'],
 'redis': ['redis[examples,redis]>=4.2.1,<5.0.0']}

setup_kwargs = {
    'name': 'fastapi-cachette',
    'version': '0.1.1',
    'description': 'Cache Implementation Extension for FastAPI Asynchronous Web Framework',
    'long_description': '# FastAPI Cachette\n\n[![Build Status](https://travis-ci.com/aekasitt/fastapi-cachette.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/fastapi-cachette)\n[![Package Vesion](https://img.shields.io/pypi/v/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![Format](https://img.shields.io/pypi/format/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![License](https://img.shields.io/pypi/l/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n\n## Features\n\nCache Implementation Extension for FastAPI Asynchronous Web Framework\nMost of the Backend implementation is directly lifted from [fastapi-cache](https://github.com/long2ice/fastapi-cache) by [@long2ice](https://github.com/long2ice)\n\n## Installation\n\nThe easiest way to start working with this extension with pip\n\n```bash\npip install fastapi-cachette\n# or\npoetry add fastapi-cachette\n```\n\n## Getting Started\n\nThe following examples show you how to integrate this extension to a FastAPI App\n\n### To Be Continued\n',
    'author': 'Sitt Guruvanich',
    'author_email': 'aekazitt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aekasitt/fastapi-cachette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
