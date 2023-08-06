# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phylum_ci', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0']}

entry_points = \
{'console_scripts': ['phylum-ci = phylum_ci.cli:main']}

setup_kwargs = {
    'name': 'phylum-ci',
    'version': '0.0.2rc5',
    'description': 'Utilities for Phylum integrations',
    'long_description': '# phylum-ci\n[![PyPI](https://img.shields.io/pypi/v/phylum-ci)](https://pypi.org/project/phylum-ci/)\n![PyPI - Status](https://img.shields.io/pypi/status/phylum-ci)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/phylum-ci)](https://pypi.org/project/phylum-ci/)\n[![GitHub](https://img.shields.io/github/license/phylum-dev/phylum-ci)](https://github.com/phylum-dev/phylum-ci/blob/main/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/phylum-dev/phylum-ci)](https://github.com/phylum-dev/phylum-ci/issues)\n![GitHub last commit](https://img.shields.io/github/last-commit/phylum-dev/phylum-ci)\n[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/phylum-dev/phylum-ci/Test/develop?label=Test&logo=GitHub)](https://github.com/phylum-dev/phylum-ci/actions/workflows/test.yml)\n\nPython package for handling CI and other integrations\n\n## Local Development\nHere\'s how to set up `phylum-ci` for local development.\n\n1. Clone the `phylum-ci` repo locally\n\n    ```sh\n    git clone git@github.com:phylum-dev/phylum-ci.git\n    ```\n\n2. Ensure all supported Python versions are installed locally\n   1. The strategy is to support all released minor versions of Python that are not end-of-life yet\n   2. The current list is 3.7, 3.8, 3.9, and 3.10, but the Python Developer\'s Guide can be referenced for the [status of active Python releases](https://devguide.python.org/#status-of-python-branches)\n   3. It is recommended to use [`pyenv`](https://github.com/pyenv/pyenv) to manage multiple Python installations\n\n    ```sh\n    # Use `pyenv install --list` to get available versions and usually install the latest patch version.\n    # NOTE: These versions are examples; the latest patch version available from pyenv should be used in place of `.x`.\n    #       example: `pyenv install --list |grep 3.9.` to show latest patch version for the cpython 3.9 minor release.\n    pyenv install 3.7.x\n    pyenv install 3.8.x\n    pyenv install 3.9.x\n    pyenv install 3.10.x\n    pyenv rehash\n    # Ensure all environments are available globally (helps tox to find them)\n    pyenv global 3.10.x 3.9.x 3.8.x 3.7.x\n    ```\n\n3. Ensure [poetry](https://python-poetry.org/docs/) is installed\n4. Install dependencies with `poetry`, which will automatically create a virtual environment:\n\n    ```sh\n    cd phylum-ci\n    poetry install\n    ```\n\n5. Create a branch for local development:\n\n    ```sh\n    git checkout -b <name-of-your-branch>\n    ```\n\n    Now you can make your changes locally.\n\n6. If new dependencies are added, ensure the `poetry.lock` file is updated (and committed):\n\n    ```sh\n    poetry lock\n    ```\n\n7. When you\'re done making changes, check that your changes pass the tests:\n\n    ```sh\n    poetry run tox\n    ```\n\n8. Commit your changes and push your branch to GitHub:\n\n    ```sh\n    git add .\n    git commit -m "Description of the changes goes here"\n    git push --set-upstream origin <name-of-your-branch>\n    ```\n\n9. Submit a pull request through the GitHub website\n',
    'author': 'Phylum, Inc.',
    'author_email': 'engineering@phylum.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://phylum.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
