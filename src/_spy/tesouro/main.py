# ! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuperPython
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# SuperPython é um software livre; você pode redistribuí-lo e/ou
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

"""Módulo principal e interface gráfica do Tesouro Inca.
.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
"""
from random import shuffle

from browser import timer

from _spy.tesouro.tesouro import Jogo
from _spy.vitollino.main import Elemento, Cena, Codigo, STYLE

# from _spy.vitollino.main import Elemento, Cena, Codigo, STYLE

STYLE["width"] = 800

DESISTE = True
PERIGOS = "aranha mumia desabe fogo cobra".split()
ARTEFATOS = "estatua vaso broche colar adorno".split()
TESOUROS = "1 2 3 4 5 5 7 7 9 11 11 13 14 15 17".split()
JOGADORES = tuple("roxanne libby sara kellee courtney angie naomi tracy morgan".split())

"""
SPRITES COM AS IMAGENS DO JOGO ORIGINAL DA GROW
===============================================
"""
SPLASH = "https://activufrj.nce.ufrj.br/studio/Introducao_a_Computacao/" \
         "Untitled_20180828_105833-0.jpg?disp=inline&size=G"
ACTIVE = "http://activufrj.nce.ufrj.br/studio/"
POS = "?disp=inline&size=G"
TEMPLOTRAS1 = ACTIVE + "Introducao_a_Computacao/Untitled_20180828_110147.jpg" + POS
IMGS = dict(
    PEDRAS4="Introducao_a_Computacao/Untitled_20180828_102220.jpg",
    PEDRAS1="Introducao_a_Computacao/Untitled_20180828_105412.jpg",
    PEDRAS3="Introducao_a_Computacao/Untitled_20180828_105419.jpg",
    PEDRAS2="Introducao_a_Computacao/Untitled_20180828_105624.jpg",
    TEMPLOTRAS1="Introducao_a_Computacao/Untitled_20180828_110147.jpg",
    TEMPLOTRAS2="Introducao_a_Computacao/Untitled_20180828_110148.jpg",
    TEMPLOTRAS3="Introducao_a_Computacao/Untitled_20180828_110145.jpg",
    CARTASENTRAESAI="Introducao_a_Computacao/Untitled_20180828_105727.jpg",
    CARTASENTRAESAITRAS="Introducao_a_Computacao/Untitled_20180828_105833-0.jpg",
    CARTASTRAS="Introducao_a_Computacao/Untitled_20180828_105833-2.jpg",
    ARTEFATOS1="Introducao_a_Computacao/Untitled_20180828_105529.jpg",
    ARTEFATOS2="Introducao_a_Computacao/Untitled_20180828_105528.jpg",
    MOSTROS="Introducao_a_Computacao/Untitled_20180828_105623.jpg",
    MOSTROS1="Introducao_a_Computacao/Untitled_20180828_105627.jpg"

)
IMGS = {key: ACTIVE + img + POS for key, img in IMGS.items()}
_SPRITES = dict(
    desabe=(IMGS["MOSTROS"], 0), aranha=(IMGS["MOSTROS"], 1), cobra=(IMGS["MOSTROS"], 2),
    fogo=(IMGS["MOSTROS1"], 0), mumia=(IMGS["MOSTROS1"], 1),
    estatua=(IMGS["ARTEFATOS1"], 0), vaso=(IMGS["ARTEFATOS1"], 1), broche=(IMGS["ARTEFATOS1"], 2),
    colar=(IMGS["ARTEFATOS2"], 0), idolo=(IMGS["ARTEFATOS2"], 1), decide=(IMGS["CARTASENTRAESAI"], 1),
    t1=(IMGS["PEDRAS1"], 0), t2=(IMGS["PEDRAS1"], 1), t4=(IMGS["PEDRAS1"], 2), t5=(IMGS["PEDRAS2"], 0),
    t7=(IMGS["PEDRAS2"], 1), t3=(IMGS["PEDRAS2"], 2), t9=(IMGS["PEDRAS3"], 0), t11=(IMGS["PEDRAS3"], 1),
    t13=(IMGS["PEDRAS3"], 2), t14=(IMGS["PEDRAS4"], 0), t15=(IMGS["PEDRAS4"], 1), t17=(IMGS["PEDRAS4"], 2),
)
SPRITES = {key: dict(img=img, index=ind, tit=key) for key, (img, ind) in _SPRITES.items()}
FASES = dict(f1=(IMGS["TEMPLOTRAS1"], 1), f2=(IMGS["TEMPLOTRAS1"], 0),
             f3=(IMGS["TEMPLOTRAS2"], 1), f4=(IMGS["TEMPLOTRAS2"], 0),
             f5=(IMGS["TEMPLOTRAS3"], 0, 800))


class Sprite(Elemento):
    def __init__(self, img, index=0, tit="", w=70, h=120, delta=210):
        super().__init__(img, style=dict(position="relative", float="left", tit=tit,
                                         width=w, height="{}px".format(h), overflow="hidden"))
        self.img.style.marginLeft = "-{}px".format(index * w)
        self.img.style.width = self.img.style.maxWidth = "{}px".format(delta)
        self.nome = "n{}".format(tit)
        "210px"
        self.w = w
        self._mostrador = None
        self._mostra = self._cria_mostra

    def __le__(self, item):
        self.elt <= item.elt

    def _cria_mostra(self, valor):
        self._mostrador = Mostrador(valor, self)
        self._mostra = self._so_mostra

    def _so_mostra(self, valor):
        self._mostrador.mostra(valor)

    def mostra(self, valor):
        self._mostra(valor)

    def face(self, index):
        self.img.style.marginLeft = "-{}px".format(index * self.w)


class Mostrador(Codigo):
    def __init__(self, display, cena):
        super().__init__(display, cena=cena)

    def mostra(self, valor):
        self._code.html = valor


class Cenario(Cena):
    def __init__(self, img, index=0, delta=1600, w=800, h=700):
        super().__init__(img)
        self.elt.style.width = w
        self.elt.style.height = "{}px".format(h)
        self.elt.style.overflow = "hidden"
        self.acampamento = Elemento("", style=dict(left=0, top=0, width=800, height="130px"))
        self.labirinto = Elemento("", style=dict(left=0, top=140, width=800, height="400px"))
        self.acampamento.nome = "Acampa"
        self.labirinto.nome = "Explora"
        self.acampamento.entra(self)
        self.labirinto.entra(self)

        self.img.style.marginLeft = "-{}px".format(index * w)
        self.img.style.width = self.img.style.maxWidth = "{}px".format(delta)
        "210px"
        self.w = w

    def reface(self, img, index, delta=1600):
        self.img.src = img
        self.img.style.marginLeft = "-{}px".format(index * self.w)
        self.img.style.width = self.img.style.maxWidth = "{}px".format(delta)
        self.labirinto.elt.html = ""

    def inicia(self):
        self.labirinto.elt.html = ""
        self.acampamento.elt.html = ""

    def face(self, index):
        self.img.style.marginLeft = "-{}px".format(index * self.w)

    def admite(self, carta):
        carta.entra(self.acampamento)

    def apresenta(self, carta):
        carta.entra(self.labirinto)


class Gui:
    _fases = [(IMGS["TEMPLOTRAS1"], 1), (IMGS["TEMPLOTRAS1"], 0),
              (IMGS["TEMPLOTRAS2"], 1), (IMGS["TEMPLOTRAS2"], 0),
              (IMGS["TEMPLOTRAS3"], 0, 800)]
    _cenario = Cenario(*(_fases[0]))

    @classmethod
    def carta(cls, face, tit=None):
        return Sprite(**SPRITES["t{}".format(face) if face.isdigit() else face])

    @classmethod
    def clear_interval(cls, interval):
        timer.clear_interval(interval)

    @classmethod
    def set_timeout(cls, rodada, param):
        timer.set_timeout(rodada, param)

    @classmethod
    def splash(cls):
        Cena(SPLASH).vai()

    @classmethod
    def inicia(cls):
        cls._cenario.inicia()

    @classmethod
    def admite(cls, carta):
        cls._cenario.admite(carta)

    @classmethod
    def apresenta(cls, carta):
        cls._cenario.apresenta(carta)

    @classmethod
    def fases(cls, indice):
        cls._cenario.reface(*(cls._fases[indice]))
        return cls._cenario

    @classmethod
    def set_interval(cls, turno, param):
        return timer.set_interval(turno, param)


GUI = Gui()


def main(jogadores=JOGADORES, gui=GUI):
    class JogadorSimples:
        def __init__(self, joga, nome):
            _chance = list(range(20))
            shuffle(_chance)
            self.joga, self.jogadas, self.nome = joga, _chance, nome
            self._inicia(nome)

        def _inicia(self, jogador):
            get_joga = "from {mod}.main import {mod}; self.joga = {mod}().joga"
            try:
                exec(get_joga.format(mod=jogador))
                self.nome = self.nome.upper()
            except (ImportError, TypeError):
                self.joga = self._joga

        def _joga(self, _):
            return self.jogadas.pop() < 2
            
    gui.inicia()
    return Jogo(gui=gui, jogadores=[JogadorSimples(None, jogador) for jogador in jogadores])



if __name__ == '__main__':
    main().inicia()
