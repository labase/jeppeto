#! /usr/bin/env python
# -*- coding: UTF8 -*-
# This file is part of  program Jeppeto
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""Sphinx document generation configuration file.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------

.. versionadded::    22.10
        Import version from code file.

"""
import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('../../src'))
from version import __version__

project = 'Jeppeto'
copyright = '2022, Carlo E. T. Oliveira'
author = 'Carlo E. T. Oliveira'

# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ["_spy/vitollino/main.py"]

language = 'pt_br'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_logo = '_static/jeppeto_logo.png'
html_theme_options = {
    'logo_only': True,
    'display_version': True,
}

html_favicon = '_static/favico.ico'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
autodoc_mock_imports = ['browser']
