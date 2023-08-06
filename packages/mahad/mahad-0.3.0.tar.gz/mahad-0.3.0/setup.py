# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maha',
 'maha.cleaners',
 'maha.cleaners.functions',
 'maha.constants',
 'maha.constants.arabic',
 'maha.constants.english',
 'maha.constants.persian',
 'maha.expressions',
 'maha.parsers',
 'maha.parsers.functions',
 'maha.parsers.rules',
 'maha.parsers.rules.duration',
 'maha.parsers.rules.numeral',
 'maha.parsers.rules.ordinal',
 'maha.parsers.rules.time',
 'maha.parsers.templates',
 'maha.processors',
 'maha.rexy',
 'maha.rexy.templates']

package_data = \
{'': ['*'], 'maha.rexy': ['cache/*']}

install_requires = \
['hijri-converter>=2.2.3,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'regex>=2021.8.28,<2022.0.0',
 'tqdm>=4.61.1,<5.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'mahad',
    'version': '0.3.0',
    'description': 'An Arabic text processing library intended for use in NLP applications.',
    'long_description': '<hr />\n<p align="center">\n    <a href="#"><img src="https://github.com/TRoboto/Maha/raw/main/images/logo.png" width= 400px></a>\n    <br />\n    <br />\n    <img src="https://github.com/TRoboto/maha/actions/workflows/ci.yml/badge.svg", alt="CI">\n    <a href=\'https://maha.readthedocs.io/en/latest/?badge=latest\'>\n    <img src=\'https://readthedocs.org/projects/maha/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n    <a href="https://codecov.io/gh/TRoboto/Maha"><img src="https://codecov.io/gh/TRoboto/Maha/branch/main/graph/badge.svg?token=9CBWXT8URA", alt="codecov"></a>\n    <a href="https://lgtm.com/projects/g/TRoboto/Maha/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/TRoboto/Maha.svg?logo=lgtm&logoWidth=18"/></a>\n    <a href="https://discord.gg/6W2tRFE7k4"><img src="https://img.shields.io/discord/863503708385312769.svg?label=discord&logo=discord" alt="Discord"></a>\n    <a href="https://pepy.tech/project/mahad"><img src="https://pepy.tech/badge/mahad/month" alt="Downloads"></a>\n    <a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="License"></a>\n    <a href="https://pypi.org/project/mahad/"><img src="https://badge.fury.io/py/mahad.svg" alt="PyPI version" height="18"></a>\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>\n    <a href="http://mypy-lang.org/"><img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy"></a>\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/mahad">\n    <br />\n    <br />\n    An Arabic text processing library intended for use in NLP applications\n\n</p>\n<hr />\n\nMaha is a text processing library specially developed to deal with Arabic text. The beta version can be used to clean and parse text, files, and folders with or without streaming capability.\n\nIf you need help or want to discuss topics related to Maha, feel free to reach out to our [Discord](https://discord.gg/6W2tRFE7k4) server. If you would like to submit a bug report or feature request, please open an issue.\n\n## Installation\n\nSimply run the following to install Maha:\n\n```bash\npip install mahad # pronounced maha d\n```\n\nFor source installation, check the [documentation](https://maha.readthedocs.io/en/latest/contributing/guidelines.html).\n\n## Overview\n\nCheck out the [overview](https://maha.readthedocs.io/en/stable/overview.html) section in the documentation to get started with Maha.\n\n## Documentation\n\nDocumentation are hosted at [ReadTheDocs](https://maha.readthedocs.io).\n\n## Contributing\n\nMaha welcomes and encourages everyone to contribute. Contributions are always appreciated. Feel free to take a look at our contribution guidelines in the [documentation](https://maha.readthedocs.io/en/latest/contributing.html).\n\n## License\n\nMaha is BSD-licensed.\n',
    'author': 'Mohammad Al-Fetyani',
    'author_email': 'm4bh@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TRoboto/Maha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
