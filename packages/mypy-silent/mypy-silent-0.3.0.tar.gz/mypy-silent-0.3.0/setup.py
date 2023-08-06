# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypy_silent']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['typer>=0.3.2,<0.4.0', 'typing-extensions']

entry_points = \
{'console_scripts': ['mypy-silent = mypy_silent.cli:cli']}

setup_kwargs = {
    'name': 'mypy-silent',
    'version': '0.3.0',
    'description': 'Silence mypy by adding or removing code comments',
    'long_description': None,
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
