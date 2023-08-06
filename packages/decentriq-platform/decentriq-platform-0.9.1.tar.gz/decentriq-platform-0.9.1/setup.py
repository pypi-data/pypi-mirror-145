# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decentriq_platform',
 'decentriq_platform.container',
 'decentriq_platform.container.proto',
 'decentriq_platform.proto',
 'decentriq_platform.sql',
 'decentriq_platform.sql.proto']

package_data = \
{'': ['*']}

install_requires = \
['asn1crypto>=1.4.0,<2.0.0',
 'certvalidator>=0.11.1,<0.12.0',
 'chily>=0.5.3,<0.6.0',
 'cryptography>=3.4.8,<4.0.0',
 'ecdsa>=0.17.0,<0.18.0',
 'oscrypto>=1.2.1,<2.0.0',
 'pem>=21.2.0,<22.0.0',
 'protobuf>=3.18.0,<4.0.0',
 'requests>=2.27.0,<3.0.0',
 'sgx-ias-structs>=0.1.7,<0.2.0',
 'sqloxide>=0.1.11,<0.2.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'decentriq-platform',
    'version': '0.9.1',
    'description': 'Python client library for the Decentriq platform',
    'long_description': '# decentriq-platform\n\nPython client library for the Decentriq platform.\n',
    'author': 'decentriq',
    'author_email': 'opensource@decentriq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decentriq/decentriq-platform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
