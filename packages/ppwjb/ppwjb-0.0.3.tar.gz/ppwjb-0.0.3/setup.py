# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ppwjb']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter==1.7.2']

extras_require = \
{':extra == "dev"': ['jupyter-book>=0.12.2,<0.13.0'],
 'dev': ['pytest>=5.4.3,<6.0.0',
         'pytest-cookies>=0.5.1,<0.6.0',
         'pyyaml>=5.3.1,<6.0.0',
         'pytest-cov>=2.10.1,<3.0.0',
         'tox>=3.20.1,<4.0.0',
         'fire>=0.4.0,<0.5.0']}

entry_points = \
{'console_scripts': ['ppwjb = ppwjb.cli:main']}

setup_kwargs = {
    'name': 'ppwjb',
    'version': '0.0.3',
    'description': 'Python project wizard with Jupyter Book',
    'long_description': "# Python Project Wizard with Jupyter Book\nA tool for creating skeleton python project, built with popular develop tools and\nconform to best practice including Jupyter Book and its various integrations.\n\n[![Version](http://img.shields.io/pypi/v/ppwjb?color=brightgreen)](https://pypi.python.org/pypi/ppwjb)\n[![CI Status](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book/actions/workflows/release.yml/badge.svg)](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book)\n[![Downloads](https://img.shields.io/pypi/dm/ppwjb)](https://pypi.org/project/ppwjb/)\n[![License](https://img.shields.io/pypi/l/ppwjb)](https://opensource.org/licenses/BSD-2-Clause)\n![Python Versions](https://img.shields.io/pypi/pyversions/ppwjb)\n\n## Features\nThis tool will create Python project with the following features:\n\n* [Poetry]: Manage version, dependency, build and release\n* [Jupyter Book]: Writing your docs in markdown style and jupyter notebooks\n* Testing with [Pytest] (unittest is still supported out of the box)\n* Code coverage report and endorsed by [Codecov]\n* [Tox]: Test your code against environment matrix, lint and artifact check.\n* Format with [Black] and [Isort]\n* Lint code with [Flake8] and [Flake8-docstrings]\n* [Pre-commit hooks]: Formatting/linting anytime when commit/run local tox/CI\n* [Bandit]: Checking for security vulnerabilities\n* Command line interface using [Python Fire] (optional)\n* Continuous Integration/Deployment by [github actions], includes:\n    - publish dev build/official release to TestPyPI/PyPI automatically when CI success\n    - publish documents automatically when CI success\n    - extract change log from github and integrate with release notes automatically\n* Host your documentation from [Git Pages] with zero-config\n\n## Quickstart\nInstall ppwjb if you haven't install it yet:\n\n```\npip install -U ppwjb\n```\n\nGenerate a Python package project by simple run:\n\n```\nppwjb\n```\n\nThen follow **[Tutorial](https://ondraz.github.io/cookiecutter-pypackage-jupyter-book/tutorial.html)** to finish other configurations.\n\n# Credits\nWe based this work on [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage)\nand borrowed some ideas from [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)\nand [briggySmalls](https://github.com/briggySmalls/cookiecutter-pypackage).\n\n[poetry]: https://python-poetry.org/\n[Jupyter Book]: https://jupyterbook.org/\n[pytest]: https://pytest.org\n[codecov]: https://codecov.io\n[tox]: https://tox.readthedocs.io\n[black]: https://github.com/psf/black\n[isort]: https://github.com/PyCQA/isort\n[flake8]: https://flake8.pycqa.org\n[flake8-docstrings]: https://pypi.org/project/flake8-docstrings/\n[mkdocstrings]: https://mkdocstrings.github.io/\n[Python Fire]: https://github.com/google/python-fire\n[github actions]: https://github.com/features/actions\n[Git Pages]: https://pages.github.com\n[Pre-commit hooks]: https://pre-commit.com/\n[Bandit]: https://bandit.readthedocs.io/en/latest/\n",
    'author': 'Ondra Zahradnik',
    'author_email': 'ondra.zahradnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ondraz/cookiecutter-pypackage-jupyter-book',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
