# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_lifecycle_flow']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0', 'packaging>=21.3,<22.0', 'urlman>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'django-lifecycle-flow',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Osmar Perez Bautista',
    'author_email': 'osmarpb.97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
