#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SupyPlay
# Copyright 2010–2022 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.activufrj.nce.ufrj.br>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# SupyPlay é um software livre; você pode redistribuí-lo e/ou
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
"""Module running WSGI interface to bottle.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    20.07
        add version file.

.. versionadded::    20.07.1
        Support import from other files.

.. versionadded::    22.09
        Run the player as default.

"""
import bottle
import os
import sys

project_home = os.path.dirname(os.path.abspath(__file__))

# add your project directory to the sys.path
# project_home = u'/home/supygirls/dev/SuPyGirls/src'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
"""Retrieves static files.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    20.07
        add version file.

.. versionadded::    20.07.1
        Support import from other files.

.. versionadded::    22.09
        Support import from other files.

"""
import bottle
from bottle import Bottle, redirect, request, get, static_file
import os
project_server = os.path.dirname(os.path.abspath(__file__))
# name and list your controllers here so their routes become accessible.
# import img_dir, js_dir, css_dir, tpl_dir
# Enable debugging, which gives us tracebacks
cod_dir = os.path.join(project_server, './')
js_dir = os.path.join(project_server, '../site/stlib')
css_dir = os.path.join(project_server, '../site/css')
img_dir = os.path.join(project_server, '../site/image')
tpl_dir = os.path.join(project_server, '../site/infra')
rot_dir = os.path.join(project_server, '../')

bottle.DEBUG = True

# Run the Bottle wsgi application. We don't need to call run() since our
# application is embedded within an App Engine WSGI application server.
appbottle = Bottle()


@appbottle.get('/x')
def home():
    """ Return Hello World at application root URL"""
    prj = request.query.proj
    print("home project /", prj)
    redirect('/main?proj=%s' % prj)


# Static Routes
@get("/")
def index():
    return static_file("index.html", root=rot_dir)


# Static Routes
@get("<_:re:.*favicon.ico>")
def favicon(_):
    return static_file("favicon.ico", root=img_dir)


# Static Routes
@get("/src/<filepath:re:.*[.](html|py)>")
def ajs(filepath):
    return static_file(filepath, root=cod_dir)


# Static Routes
@get("/site/infra/<filepath:re:.*[.](html|tpl)>")
def ajs(filepath):
    return static_file(filepath, root=tpl_dir)


# Static Routes
@get("/site/css/<filepath:re:.*[.](js|css)>")
def ajs(filepath):
    return static_file(filepath, root=css_dir)


# Static Routes
@get("/css/<filepath:re:.*[.](js|css|map)>")
def ajs(filepath):
    return static_file(filepath, root=css_dir)


# Static Routes
@get("/js/<filepath:re:.*[.](js|css)>")
def ajs(filepath):
    return static_file(filepath, root=js_dir)


# Static Routes
@get("<filepath:re:.*[.](js|css)>")
def js(filepath):
    return static_file(filepath, root=js_dir)


# Static Routes
@get("/site/image/<filepath:re:.*[.](png|jpg|svg|gif|ico)>")
def img(filepath):
    return static_file(filepath, root=img_dir)


@appbottle.error(code=404)
def error_404(_):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'


if __name__ == "__main__":
    bottle.run(host='localhost', port=8080, debug=True)
