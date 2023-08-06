# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['juselara_qtile']

package_data = \
{'': ['*']}

install_requires = \
['cairocffi>=1.3.0,<2.0.0',
 'cffi>=1.15.0,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'qtile>=0.21.0,<0.22.0',
 'xcffib>=0.11.1,<0.12.0',
 'yacmmal>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'juselara-qtile',
    'version': '0.1.1',
    'description': 'My setup for the Qtile window manager',
    'long_description': None,
    'author': 'Juan Lara',
    'author_email': 'julara@unal.edu.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8,<3.11',
}


setup(**setup_kwargs)
