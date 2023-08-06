# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nerddiary',
 'nerddiary.asynctools',
 'nerddiary.client',
 'nerddiary.data',
 'nerddiary.error',
 'nerddiary.job',
 'nerddiary.poll',
 'nerddiary.primitive',
 'nerddiary.report',
 'nerddiary.server',
 'nerddiary.server.api',
 'nerddiary.server.api.api_v1',
 'nerddiary.server.api.api_v1.routers',
 'nerddiary.server.mixins',
 'nerddiary.server.session',
 'nerddiary.user',
 'nerddiary.utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.2,<2.0.0',
 'pydantic[dotenv]>=1.9.0,<2.0.0',
 'pytz>=2022.1,<2023.0',
 'websockets>=10.1,<11.0']

extras_require = \
{'client': ['jsonrpcclient>=4.0.2,<5.0.0'],
 'full': ['jsonrpcclient>=4.0.2,<5.0.0',
          'jsonrpcserver>=5.0.6,<6.0.0',
          'click>=8.0.3,<9.0.0',
          'SQLAlchemy>=1.4.29,<2.0.0',
          'cryptography>=36.0.1,<37.0.0',
          'APScheduler>=3.8.1,<4.0.0',
          'uvicorn>=0.17.4,<0.18.0',
          'fastapi>=0.75.0,<0.76.0'],
 'server': ['jsonrpcserver>=5.0.6,<6.0.0',
            'click>=8.0.3,<9.0.0',
            'SQLAlchemy>=1.4.29,<2.0.0',
            'cryptography>=36.0.1,<37.0.0',
            'APScheduler>=3.8.1,<4.0.0',
            'uvicorn>=0.17.4,<0.18.0',
            'fastapi>=0.75.0,<0.76.0']}

entry_points = \
{'console_scripts': ['nerddiary = nerddiary.cli:cli']}

setup_kwargs = {
    'name': 'nerddiary',
    'version': '0.2.2a0',
    'description': 'A collection of tools to capture a personal log / diary and analyze these records',
    'long_description': '# The Nerd Diary\n\n[![pypi](https://img.shields.io/pypi/v/nerddiary.svg)](https://pypi.org/project/nerddiary/)\n[![python](https://img.shields.io/pypi/pyversions/nerddiary.svg)](https://pypi.org/project/nerddiary/)\n[![Build Status](https://github.com/mishamsk/nerddiary/actions/workflows/dev.yml/badge.svg)](https://github.com/mishamsk/nerddiary/actions/workflows/dev.yml)\n\nTBD\n\n\n* Documentation: <https://mishamsk.github.io/nerddiary>\n* GitHub: <https://github.com/mishamsk/nerddiary>\n* PyPI: <https://pypi.org/project/nerddiary/>\n* Free software: Apache-2.0\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was inspired by the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template and others.\n',
    'author': 'mishamsk',
    'author_email': 'mishamsk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nerddiary.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
