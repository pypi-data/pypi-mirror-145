# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fitbit', 'fitbit.api', 'fitbit.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=14.05.14',
 'click>=8.0.1',
 'python-dateutil>=2.5.3',
 'python-dotenv>=0.19.2,<0.20.0',
 'setuptools>=21.0.0',
 'six>=1.10',
 'urllib3>=1.15.1']

entry_points = \
{'console_scripts': ['py-fitbit = fitbit.__main__:main']}

setup_kwargs = {
    'name': 'py-fitbit',
    'version': '1.0.1',
    'description': 'Python bindings for Fitbit Web API',
    'long_description': "# Python bindings of Fitbit WebAPI\n\n[![PyPI](https://img.shields.io/pypi/v/py-fitbit.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/py-fitbit.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/py-fitbit)][python version]\n[![License](https://img.shields.io/pypi/l/py-fitbit)][license]\n\n[![Read the documentation at https://py-fitbit.readthedocs.io/](https://img.shields.io/readthedocs/py-fitbit/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/j-rossi-nl/py-fitbit/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/j-rossi-nl/py-fitbit/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/py-fitbit/\n[status]: https://pypi.org/project/py-fitbit/\n[python version]: https://pypi.org/project/py-fitbit\n[read the docs]: https://py-fitbit.readthedocs.io/\n[tests]: https://github.com/j-rossi-nl/py-fitbit/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/j-rossi-nl/py-fitbit\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Python bindings of Fitbit WebAPI_ via [pip] from [PyPI]:\n\n```console\n$ pip install py-fitbit\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Python bindings of Fitbit WebAPI_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/j-rossi-nl/py-fitbit/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/j-rossi-nl/py-fitbit/blob/main/LICENSE\n[contributor guide]: https://github.com/j-rossi-nl/py-fitbit/blob/main/CONTRIBUTING.md\n[command-line reference]: https://py-fitbit.readthedocs.io/en/latest/usage.html\n",
    'author': 'Team',
    'author_email': 'j.rossi@uva.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j-rossi-nl/py-fitbit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
