#! /usr/bin/env python
# -*- coding: UTF8 -*-
# This file is part of  program Jeppeto
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Jeppeto - Classes empacotadoras.

    Classes neste módulo:
        - :py:class:`Boxer`     Estrutura uma caixa com dimensões e tipo.
        - :py:class:`Box`       Empacota uma estrutura do tipo :py:class:`Boxer`.
        - :py:class:`ModelMake` Fachada de criação dos empacotadores de componentes.
        - :py:class:`Tomada`    Empacota o componente Vitollino Cena.
        - :py:class:`Ator`      Empacota o componente Vitollino Elemento.
        - :py:class:`Objeto`    Empacota o componente Vitollino Elemento passivo.
        - :py:class:`Fala`      Empacota o componente Vitollino Texto.
        - :py:class:`Quarto`    Empacota o componente Vitollino Sala.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.10
        Separa as classes envoltórias do módulo editor.

.. versionadded::    22.10a
        Documenta as classes.

"""

from _spy.vitollino.main import Cena, Elemento, Texto, Sala  # , Labirinto
# from _spy.vitollino.main import INVENTARIO as inv
# from browser import svg, document, html, alert
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
NO_BOX = Boxer(0, 0, 0, 100, 60)
"""An empty boxer instance."""


class Box:
    """Represents a generic box appearing in screen.

    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """
    BOX = []
    """Static collection of boxes reuniting all box instances created."""

    def __init__(self, box=NO_BOX):
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
        """ Remove the box from collection.

        :param box: reference to the box to be removed.
        :return: None
        """
        _ = self
        Box.BOX.remove(box)

    def as_dict(self):
        """Return the box as a dictionary.

        :return: dictionary with box fields as keys.
        """
        b = self.box
        return dict(f=b.f, x=b.x, y=b.y, w=b.w, h=b.h)

    def find(self, x, y):
        """ Return the box located at this coordinate.

        :param x: x coordinate.
        :param y: y coordinate.
        :return: the box found at given coordinate.
        """
        _ = self
        for bbox in Box.BOX:
            box = bbox.box
            if (box.x < x < box.x + box.w) and (box.y < y < box.y + box.h):
                return bbox
        return None


class Tomada(Cena, Box):
    """Wraps Vitollino class Cena.

    :param img: reference to a picture file.
    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """

    def __init__(self, img='', box=NO_BOX):
        Cena.__init__(self, img)
        Box.__init__(self, box)


class Ator(Elemento, Box):
    """Wraps Vitollino class Elemento.

    :param img: reference to a picture file.
    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """

    def __init__(self, img='', cena='', box=NO_BOX):
        Elemento.__init__(self, img, cena=cena)
        Box.__init__(self, box)


class Objeto(Elemento, Box):
    """Wraps Vitollino class Elemento as passive component.

    :param img: reference to a picture file.
    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """

    def __init__(self, img='', cena='', box=NO_BOX):
        Elemento.__init__(self, img, cena=cena)
        Box.__init__(self, box)


class Fala(Texto, Box):
    """Wraps Vitollino class Texto.

    :param cena: reference to a Cena instance.
    :param fala: string to be written in the dialog.
    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """

    def __init__(self, cena='', fala='', box=NO_BOX):
        Texto.__init__(self, cena, fala)
        Box.__init__(self, box)


class Quarto(Sala, Box):
    """Wraps Vitollino class Sala.

    :param salas: dictionary {n, s, l, o} with Cena instances .
    :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
    """

    def __init__(self, salas=None, box=NO_BOX):
        Sala.__init__(self, **salas)
        Box.__init__(self, box)


class ModelMake(Box):
    """Fachada de acesso aos empacotadores de componentes.

    :param gui: referência ao módulo de apresentação gráfica.
    """

    def __init__(self, gui):

        super().__init__()
        self.gui = gui
        self.parts = dict(tomada=self.tomada, ator=self.ator, objeto=self.objeto, texto=self.texto, sala=self.sala)

    def paint(self, box=NO_BOX, **kwargs):
        """Paint the box on the canvas.

        :param kwargs:  extra arguments.
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        """
        if box.f not in self.parts:
            return
        box = self.parts[box.f](box=box, **kwargs)
        Box.BOX.append(box)

    def tomada(self, img='', box=NO_BOX):
        """Wraps Vitollino class Cena.

        :param img: reference to a picture file.
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        :return: instance of Tomada.
        """
        _ = self
        return Tomada(img=img, box=box)

    def ator(self, img='', box=NO_BOX):
        """Wraps Vitollino class Elemento.

        :param img: reference to a picture file.
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        :return: instance of Ator.
        """
        _ = self
        return Ator(img=img, box=box)

    def objeto(self, img='', box=NO_BOX):
        """Wraps Vitollino class Elemento as passive.

        :param img: reference to a picture file.
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        :return: instance of Objeto.
        """
        _ = self
        return Objeto(img=img, box=box)

    def texto(self, cena='', box=NO_BOX):
        """Wraps Vitollino class Texto.

        :param cena: reference to a Cena instance.
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        :return: instance of Fala.
        """
        _ = self
        return Fala(cena=cena, box=box)

    def sala(self, salas=None, box=NO_BOX):
        """Wraps Vitollino class Sala.

        :param salas: dictionary {n, s, l, o} with Cena instances .
        :param box: namedtuple of :func:`jeppeto.wrapper.Boxer` type.
        :return: instance of Quarto.
        """
        _ = self
        return Quarto(salas=salas, box=box)
