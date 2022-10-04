#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Jeppeto
# Copyright 2010–2022 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.activufrj.nce.ufrj.br>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# Jeppeto é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>
"""Module module wide names.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.10
        Fix for Jeppeto tree layout.

"""
import os
# name and list your controllers here so their routes become accessible.
# Enable debugging, which gives us tracebacks
project_server = os.path.dirname(os.path.abspath(__file__))
js_dir = os.path.join(project_server, '../site/stlib')
css_dir = os.path.join(project_server, '../site/css')
img_dir = os.path.join(project_server, '../site/image')
tpl_dir = os.path.join(project_server, '../site/tpl')
# py_dir = os.path.join(project_server, '../view')
# model_dir = os.path.join(project_server, '../model')
print("js_dir = ", js_dir)
