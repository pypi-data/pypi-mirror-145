# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_loader',
 'code_loader.contract',
 'code_loader.dataset_binder',
 'code_loader.decoders']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses==0.8', 'numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'code-loader',
    'version': '0.2.12',
    'description': '',
    'long_description': '# tensorleap code loader\nUsed to load user code to tensorleap \n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensorleap/code-loader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.7',
}


setup(**setup_kwargs)
