# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volley', 'volley.connectors', 'volley.models', 'volley.serializers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'msgpack>=1.0.3,<2.0.0',
 'orjson>=3.6.4,<4.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'pydantic>=1.8.2,<2.0.0']

extras_require = \
{'all': ['confluent-kafka>=1.8.2,<2.0.0',
         'PyRSMQ>=0.4.5,<0.5.0',
         'hiredis>=2.0.0,<3.0.0',
         'tenacity>=8.0.1,<9.0.0',
         'pyzmq>=22.3.0,<23.0.0'],
 'kafka': ['confluent-kafka>=1.8.2,<2.0.0'],
 'rsmq': ['PyRSMQ>=0.4.5,<0.5.0',
          'hiredis>=2.0.0,<3.0.0',
          'tenacity>=8.0.1,<9.0.0'],
 'zmq': ['pyzmq>=22.3.0,<23.0.0']}

setup_kwargs = {
    'name': 'py-volley',
    'version': '0.17.2',
    'description': 'Pluggable message queueing for Python',
    'long_description': None,
    'author': 'ask-machine-learning',
    'author_email': 'shipt@shipt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
