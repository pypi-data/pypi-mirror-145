# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smartworks', 'smartworks.ecp']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=7.1.0,<8.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.6.7,<4.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'altair-smartworks-ecp-client',
    'version': '0.5.3',
    'description': 'Altair SmartWorks IoT Edge Compute Platform client',
    'long_description': 'Altair SmartWorks IoT Edge Compute Platform client\n',
    'author': 'Javier Holgueras Crespo',
    'author_email': 'jholgueras@europe.altair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/swx-main/smartworks-iot/pocs/people-counter/ecp-python-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
