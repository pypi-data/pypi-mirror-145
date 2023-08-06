# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cachette', 'fastapi_cachette.backends', 'fastapi_cachette.codecs']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'dynamodb': ['aiobotocore[dynamodb,examples]>=2.2.0,<3.0.0'],
 'examples': ['uvicorn[examples]==0.15.0',
              'aiomcache[memcached,examples]>=0.7.0,<0.8.0',
              'aiobotocore[dynamodb,examples]>=2.2.0,<3.0.0',
              'redis[examples,redis]>=4.2.1,<5.0.0'],
 'memcached': ['aiomcache[memcached,examples]>=0.7.0,<0.8.0'],
 'mongodb': ['motor[mongodb,examples]>=2.5.1,<3.0.0'],
 'msgpack': ['msgpack[msgpack]>=1.0.3,<2.0.0'],
 'orjson': ['orjson[orjson]>=3.6.7,<4.0.0'],
 'redis': ['redis[examples,redis]>=4.2.1,<5.0.0']}

setup_kwargs = {
    'name': 'fastapi-cachette',
    'version': '0.1.2',
    'description': 'Cache Implementation Extension for FastAPI Asynchronous Web Framework',
    'long_description': '# FastAPI Cachette\n\n[![Build Status](https://travis-ci.com/aekasitt/fastapi-cachette.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/fastapi-cachette)\n[![Package Vesion](https://img.shields.io/pypi/v/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![Format](https://img.shields.io/pypi/format/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n[![License](https://img.shields.io/pypi/l/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)\n\n## Features\n\nCache Extension for FastAPI Asynchronous Web Framework\nMost of the Backend implementation is directly lifted from \n[fastapi-cache](https://github.com/long2ice/fastapi-cache) by \n[@long2ice](https://github.com/long2ice) excluding the MongoDB backend option.\n\n## Upcoming Features (To-Do List)\n\n1. Implement `flush` and `flush_expired` methods on individual backends \n(Not needed for Redis & Memcached backends)\n\n2. Implement options for encoding/decoding cache data using built-in protocols such as pickle, json\nor third-party protocol such as msgpack, parquet, feather, hdf5\n\n3. Write more examples\n\n## Installation\n\nThe easiest way to start working with this extension with pip\n\n```bash\npip install fastapi-cachette\n# or\npoetry add fastapi-cachette\n```\n\n## Getting Started\n\nThis FastAPI extension utilizes "Dependency Injection" (To be continued)\n\nConfiguration of this FastAPI extension must be done at startup using "@Cachette.load_config" \ndecorator (To be continued)\n\nThese are all available options with explanations and validation requirements (To be continued)\n\n## Examples\n\nThe following examples show you how to integrate this extension to a FastAPI App (To be continued)\n\nSee "examples/" folders\n\nTo run examples, first you must install extra dependencies\n\nDo all in one go with this command...\n\n```bash\npip install aiobotocore aiomcache motor uvicorn redis\n# or\npoetry install --extras examples\n```\n\nDo individual example with this command...\n\n```bash\npip install redis\n# or\npoetry install --extras redis\n# or\npoetry install --extras `<example-name>`\n```\n\n## Contributions\n\nSee features and write tests I guess.\n\n## Test Environment Setup\n\nThis project utilizes multiple external backend services namely AWS DynamoDB, Memcached, MongoDB and\nRedis as backend service options as well as a possible internal option called InMemoryBackend. In\norder to test viability, we must have specific instances of these set up in the background of our\ntesting environment \n\n### With Docker-Compose\n\nUtilize orchestration file attached to reposity and `docker-compose` command to set up testing \ninstances of backend services using the following command...\n\n```bash\ndocker-compose up -d\n```\n\nWhen you are finished, you can stop and remove background running backend instances with the\nfollowing command...\n\n```bash\ndocker-compose down\n```\n\n### Without Docker-Compose\n\nIf you are using `arm64` architecture on your local machine like I am with my fancy MacBook Pro, \nthere is a chance that your `docker-compose` (V1) is not properly configured and have caused you \nmany headaches. The following commands will allow you to replicate docker-compose orchestration\ncommand given above.\n\n\n1. AWS DynamoDB Local\n\n    ```bash\n    docker run --detach --rm -ti -p 8000:8000 --name cachette-dynamodb amazon/dynamodb-local:latest\n    ```\n\n2. Memcached\n\n    ```bash\n    docker run --detach --rm -ti -p 11211:11211 --name cachette-memcached memcached:bullseye\n    ```\n\n3. MongoDB\n\n    ```bash\n    docker run --detach --rm -ti -p 27017:27017 --name cachette-mongodb mongo:latest\n    ```\n\n4. Redis\n\n    ```bash\n    docker run --detach --rm -ti -p 6379:6379 --name cachette-redis redis:bullseye\n    ```\n\nAnd finally, to stop and remove running instances, run the following command\n\n```bash\n[ -n $(docker ps -f name="cachette-*" -q) ] && docker kill $(docker ps -f name="cachette-*" -q)\n```\n\n## Tests\n\nNow that you have background running backend instances, you can proceed with the tests by using\n`pytest` command as such...\n\n```bash\npytest\n```\n\nOr you can configure the command to run specific tests as such...\n\n```bash\npytest -k test_load_invalid_configs\n# or\npytest -k test_set_then_clear\n```\n\nAll test suites must be placed under `tests/` folder or its subfolders.\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
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
