..  # This file is part of  program Jeppeto
    # Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
    # `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
    # SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
.. _modulo_wrapper:

Módulo Empacotador
------------------
Define um conjunto de classes que empacotam componentes da biblioteca Vitollino.

Classes Empacotadoras
^^^^^^^^^^^^^^^^^^^^^
Empacotam componentes do Vitollino.

.. automodule:: jeppeto.wrapper
    :members:
    :undoc-members:
    :show-inheritance:
    :platform: Web
    :synopsis: Empacotamento de componentes gráficos.
    :exclude-members: Boxer, ModelMake

Classe Auxiliar Boxer
^^^^^^^^^^^^^^^^^^^^^
Define parâmetros para a construção de um dado elemento.

.. autoclass:: jeppeto.wrapper.Boxer
    :no-undoc-members:

Fachada Criadora ModelMake
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fachada que reúne comandos para criar classes empacotadoras.

Estas classes reúnem o elemento original do Vitollino com uma classe Boxer.
Com isto, os componentes podem ser representados simbolicamente na tela
do Jeppeto

.. autoclass:: jeppeto.wrapper.ModelMake
    :members:
    :undoc-members:
    :show-inheritance:

.. seealso::

   Module :ref:`modulo_main`

.. note::
   Cria classes empacotadoras para a biblioteca Vitollino.

.. include:: foot.rst
