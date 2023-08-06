# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speedscope_to_codeperf', 'speedscope_to_codeperf.schema']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'pandas>=1.4.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['speedscope-to-codeperf = '
                     'speedscope_to_codeperf.cli:main']}

setup_kwargs = {
    'name': 'speedscope-to-codeperf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'filipecosta90',
    'author_email': 'filipecosta.90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
