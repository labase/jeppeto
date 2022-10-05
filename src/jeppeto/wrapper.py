#! /usr/bin/env python
# -*- coding: UTF8 -*-
# This file is part of  program Jeppeto
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Jeppeto - Classes empacotadoras.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------

.. versionadded::    22.10
        Separa as classes envoltórias do módulo editor.

"""

from _spy.vitollino.main import Cena, Elemento, Texto, Sala, Labirinto
# from _spy.vitollino.main import INVENTARIO as inv
from browser import svg, document, html, alert
from collections import namedtuple
Boxer = namedtuple('Boxer', ['f', 'x', 'y', 'w', 'h'])
""" Specification of Box attributes.

.. py:attribute:: f
    the kind representation of the box

.. py:attribute:: x
    horizontal displacement

.. py:attribute:: y
    vertical displacement

.. py:attribute:: w
    horizontal size of the box

.. py:attribute:: h
    vertical size of the box

"""
NOBOX = Boxer(0, 0, 0, 100, 60)

# "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.1.2/css/fontawesome.min.css"
AWESOME = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css"
FAW = html.LINK(rel="stylesheet", href=AWESOME, Type="text/css")
FAW.setAttribute("type", "text/css")
JEPPETO = "https://i.imgur.com/eI50beC.png"
_ = document.head <= FAW


class Box:
    """Represents a generic box appearing in screen.

    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """
    BOX = []

    def __init__(self, box=NOBOX):
        # Box.BOX = []
        self.box = box

    def paint(self, f=None, **kwargs):
        """Paint the box on the canvas.

        :param f: function of this box.
        :param kwargs: parameters to forward to renderer.
        :return: None.
        """
        _ = self
        box = Box(Boxer(f=f, **kwargs))
        Box.BOX.append(box)

    def remove(self, box):
        """
        Remove the box from collection.
        :param box: reference to the box to be removed.
        :return:
        """
        _ = self
        Box.BOX.remove(box)

    def as_dict(self):
        b = self.box
        return dict(f=b.f, x=b.x, y=b.y, w=b.w, h=b.h)

    def find(self, x, y):
        _ = self
        for bbox in Box.BOX:
            box = bbox.box
            if (box.x < x < box.x + box.w) and (box.y < y < box.y + box.h):
                return bbox
        return None


class Tomada(Cena, Box):
    def __init__(self, img='', box=NOBOX):
        Cena.__init__(self, img)
        Box.__init__(self, box)


class Ator(Elemento, Box):
    def __init__(self, img='', cena='', box=NOBOX):
        Elemento.__init__(self, img, cena=cena)
        Box.__init__(self, box)


class Objeto(Elemento, Box):
    def __init__(self, img='', cena='', box=NOBOX):
        Elemento.__init__(self, img, cena=cena)
        Box.__init__(self, box)


class Fala(Texto, Box):
    def __init__(self, cena='', fala='', box=NOBOX):
        Texto.__init__(self, cena, fala)
        Box.__init__(self, box)


class Quarto(Sala, Box):
    def __init__(self, img='', box=NOBOX):
        Sala.__init__(self, img)
        Box.__init__(self, box)


class ModelMake:
    """Fachada de acesso aos empacotadores de componentes.

    :param gui: referência ao módulo de interface gráfica.
    """

    def __init__(self, gui):

        self.gui = gui
        self.parts = dict(tomada=self.tomada, ator=self.ator, objeto=self.objeto, texto=self.texto, sala=self.sala)

    def paint(self, box=NOBOX, **kwargs):
        if box.f not in self.parts:
            return
        box = self.parts[box.f](box=box, **kwargs)
        Box.BOX.append(box)

    def tomada(self, img='', box=NOBOX):
        _ = self
        return Tomada(img=img, box=box)

    def ator(self, img='', box=NOBOX):
        _ = self
        return Ator(img=img, box=box)

    def objeto(self, img='', box=NOBOX):
        _ = self
        return Objeto(img=img, box=box)

    def texto(self, cena='', box=NOBOX):
        _ = self
        return Fala(cena=cena, box=box)

    def sala(self, img='', box=NOBOX):
        _ = self
        return Quarto(img=img, box=box)
