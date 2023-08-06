# Python Project Wizard with Jupyter Book
A tool for creating skeleton python project, built with popular develop tools and
conform to best practice including Jupyter Book and its various integrations.

[![Version](http://img.shields.io/pypi/v/ppwjb?color=brightgreen)](https://pypi.python.org/pypi/ppwjb)
[![CI Status](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book/actions/workflows/release.yml/badge.svg)](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book)
[![Downloads](https://img.shields.io/pypi/dm/ppwjb)](https://pypi.org/project/ppwjb/)
[![License](https://img.shields.io/pypi/l/ppwjb)](https://opensource.org/licenses/BSD-2-Clause)
![Python Versions](https://img.shields.io/pypi/pyversions/ppwjb)

## Features
This tool will create Python project with the following features:

* [Poetry]: Manage version, dependency, build and release
* [Jupyter Book]: Writing your docs in markdown style and jupyter notebooks
* Testing with [Pytest] (unittest is still supported out of the box)
* Code coverage report and endorsed by [Codecov]
* [Tox]: Test your code against environment matrix, lint and artifact check.
* Format with [Black] and [Isort]
* Lint code with [Flake8] and [Flake8-docstrings]
* [Pre-commit hooks]: Formatting/linting anytime when commit/run local tox/CI
* [Bandit]: Checking for security vulnerabilities
* Command line interface using [Python Fire] (optional)
* Continuous Integration/Deployment by [github actions], includes:
    - publish dev build/official release to TestPyPI/PyPI automatically when CI success
    - publish documents automatically when CI success
    - extract change log from github and integrate with release notes automatically
* Host your documentation from [Git Pages] with zero-config

## Quickstart
Install ppwjb if you haven't install it yet:

```
pip install -U ppwjb
```

Generate a Python package project by simple run:

```
ppwjb
```

Then follow **[Tutorial](https://ondraz.github.io/cookiecutter-pypackage-jupyter-book/tutorial.html)** to finish other configurations.

# Credits
We based this work on [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage)
and borrowed some ideas from [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
and [briggySmalls](https://github.com/briggySmalls/cookiecutter-pypackage).

[poetry]: https://python-poetry.org/
[Jupyter Book]: https://jupyterbook.org/
[pytest]: https://pytest.org
[codecov]: https://codecov.io
[tox]: https://tox.readthedocs.io
[black]: https://github.com/psf/black
[isort]: https://github.com/PyCQA/isort
[flake8]: https://flake8.pycqa.org
[flake8-docstrings]: https://pypi.org/project/flake8-docstrings/
[mkdocstrings]: https://mkdocstrings.github.io/
[Python Fire]: https://github.com/google/python-fire
[github actions]: https://github.com/features/actions
[Git Pages]: https://pages.github.com
[Pre-commit hooks]: https://pre-commit.com/
[Bandit]: https://bandit.readthedocs.io/en/latest/
