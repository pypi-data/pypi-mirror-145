# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/test/python'}

packages = \
['python', 'python.dev4py.utils']

package_data = \
{'': ['*']}

modules = \
['project']
setup_kwargs = {
    'name': 'dev4py-utils',
    'version': '1.0.1',
    'description': 'A set of Python regularly used classes/functions',
    'long_description': '# Dev4py-utils\n\nA set of Python regularly used classes/functions\n\n[![ci](https://github.com/dev4py/dev4py-utils/actions/workflows/ci.yml/badge.svg?event=push&branch=main)](https://github.com/dev4py/dev4py-utils/actions/workflows/ci.yml) <br/>\n[![Last release](https://github.com/dev4py/dev4py-utils/actions/workflows/on_release.yml/badge.svg)](https://github.com/dev4py/dev4py-utils/actions/workflows/on_release.yml) <br/>\n[![Weekly checks](https://github.com/dev4py/dev4py-utils/actions/workflows/weekly_checks.yml/badge.svg?branch=main)](https://github.com/dev4py/dev4py-utils/actions/workflows/weekly_checks.yml) <br/>\n[![Python >= 3.10.1](https://img.shields.io/badge/Python->=3.10.1-informational.svg?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/) <br/>\n[![Maintainer](https://img.shields.io/badge/maintainer-St4rG00se-informational?style=plastic&logo=superuser)](https://github.com/St4rG00se) <br/>\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=plastic&logo=github)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) <br/>\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=plastic&logo=github)](https://opensource.org/licenses/MIT)\n\n\n## Project template\n\nThis project is based on [pymsdl_template](https://github.com/dev4py/pymsdl_template)\n\n## Project links\n\n* [Documentation](https://htmlpreview.github.io/?https://github.com/dev4py/dev4py-utils/blob/main/docs/index.html)\n* [PyPi project](https://pypi.org/project/dev4py-utils/)\n',
    'author': 'St4rG00se',
    'author_email': 'st4rg00se@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dev4py/dev4py-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
