# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watson_overtime']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<9.0.0', 'humanize>=3.14.0,<5.0.0', 'pytimeparse>=1.1.8,<2.0.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata==4.2.0']}

entry_points = \
{'console_scripts': ['watson-overtime = watson_overtime.main:main']}

setup_kwargs = {
    'name': 'watson-overtime',
    'version': '0.3.0',
    'description': 'Check overtime in combination with the td-watson time tracker',
    'long_description': '[![Tests](https://github.com/flyingdutchman23/watson-overtime/workflows/Tests/badge.svg)](https://github.com/flyingdutchman23/watson-overtime/actions?workflow=Tests)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/flyingdutchman23/watson-overtime/main.svg)](https://results.pre-commit.ci/latest/github/flyingdutchman23/watson-overtime/main)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Python Versions](https://img.shields.io/pypi/pyversions/watson-overtime)](https://img.shields.io/pypi/pyversions/watson-overtime)\n\n\n# watson-overtime\n\n\n## Description\n\nThis is a simple tool to calculate if a set working time is fulfilled for a\ncertain period of time. Therefore, it uses the time tracking software\n[td-watson][https://pypi.org/project/td-watson/] as input.\n\n\n## Usage\n\nGenerate a `watson report` in JSON format. This command e.g. generates a watson\nreport for the current for the project `PROJECT`. Pipe the output to\n`watson-overtime`:\n```bash\nwatson report -w -p PROJECT --json | watson-overtime\n```\n',
    'author': 'Joris Clement',
    'author_email': 'flyingdutchman@posteo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flyingdutchman23/watson-overtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
