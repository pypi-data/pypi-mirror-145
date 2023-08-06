"""Common functions for Python / Vue / Eel project.

.. image:: https://img.shields.io/pypi/pyversions/pyvueeel.svg
    :target: https://pypi.python.org/pypi/pyvueeel/
    :alt: Python versions

.. image:: https://badge.fury.io/py/pyvueeel.svg
    :target: https://badge.fury.io/py/pyvueeel
    :alt: PyPI version

.. image:: https://pepy.tech/badge/pyvueeel
    :target: https://pepy.tech/project/pyvueeel
    :alt: Downloads

.. image:: https://img.shields.io/lgtm/grade/python/github/Malachov/pyvueeel.svg
    :target: https://lgtm.com/projects/g/Malachov/pyvueeel/context:python
    :alt: Language grade: Python

.. image:: https://readthedocs.org/projects/pyvueeel/badge/?version=latest
    :target: https://pyvueeel.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT

.. image:: https://codecov.io/gh/Malachov/pyvueeel/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Malachov/pyvueeel
    :alt: Codecov

It contains functions for running eel, overriding eel.expose decorator, converting json to correct python
format or transform data into form for vue tables and plots.

Try [cookiecutter template](https://github.com/Malachov/project-starter-cookiecutter) for working examples.

Image of such an app

.. image:: /_static/project-starter-gui.png
    :width: 620
    :alt: project-starter-gui
    :align: center


Links
=====

Official documentation - https://pyvueeel.readthedocs.io/

Official repo - https://github.com/Malachov/pyvueeel

Installation
============

Python >=3.6 (Python 2 is not supported).

Install with::

    pip install pyvueeel
"""
import mylogging as __mylogging

import EelForkExcludeFiles as eel

from pyvueeel.pyvueeel_internal import (
    expose,
    expose_error_callback,
    json_to_py,
    run_gui,
    to_table,
    to_vue_plotly,
)

__all__ = [
    "expose",
    "eel",
    "expose_error_callback",
    "json_to_py",
    "run_gui",
    "to_table",
    "to_vue_plotly",
]

__version__ = "0.0.5"

__author__ = "Daniel Malachov"
__license__ = "MIT"
__email__ = "malachovd@seznam.cz"

__mylogging.my_traceback.enhance_excepthook()
