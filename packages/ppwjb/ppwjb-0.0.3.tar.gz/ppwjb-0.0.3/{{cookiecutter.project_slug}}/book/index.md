{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
# {{ cookiecutter.project_name }}

{% if is_open_source %}
[![Version](http://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}?color=brightgreen)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})
[![CI Status](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
[![Downloads](https://img.shields.io/pypi/dm/{{ cookiecutter.project_slug }})](https://pypi.org/project/{{ cookiecutter.project_slug }}/)
[![License](https://img.shields.io/pypi/l/{{ cookiecutter.project_slug }})](https://opensource.org/licenses/{{ cookiecutter.open_source_license }})
![Python Versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }})

{% if cookiecutter.add_pyup_badge == 'y' %}
[![pyup](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{%- endif %}
{%- endif %}

Skeleton project created with [Python Project Wizard (ppwjb)](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book) with [Jupyter Book](https://jupyterbook.org/) pre-configured.

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
{%- endif %}

## Features

* TODO

## Credits

This package was created with following project templates.

* [ondraz/cookiecutter-pypackage-jupyter-book](https://github.com/ondraz/cookiecutter-pypackage-jupyter-book)
* [audreyr/cookiecutter](https://github.com/audreyr/cookiecutter)
* [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage)
