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

"""
    Módulo central com a lógica do jogo do Tesouro Inca.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from random import shuffle

DESISTE = True
PERIGOS = "aranha mumia desabe fogo cobra".split()
ARTEFATOS = "estatua vaso broche colar idolo".split()
TESOUROS = "1 2 3 4 5 5 7 7 9 11 11 13 14 15 17".split()
JOGADORES = tuple((None, player) for player in "roxanne libby sara kellee courtney angie naomi tracy morgan".split())
GET_JOGADOR = "from {mod}.main import {mod}; self.jogador = {mod}()"


class Carta(object):
    """
        Carta que genérica que pode ser um perigo, artefato ou tesouro.

    :param face: Índice do sprite que representa esta carta.
    """
    PERIGO = []
    VALOR = 2

    def __init__(self, face):
        self.face = face
        self.valor = int(face) if face.isdigit() else 0
        self.elt = Jogo.GUI.carta(face)

    def termina(self, salas):
        return False

    def premia(self, jogadores, _):
        return True

    def inicia(self):
        self.valor = int(self.face) if self.face.isdigit() else 0

    def mostra(self):
        return True

    def atualiza_saldo(self, divider):
        self.valor = (self.valor % divider) if divider else self.valor
        self.mostra()

    def divide(self, jogadores, salas):
        for sala in salas:
            sala.divide_valor(jogadores, sala)

    def divide_valor(self, jogadores, sala):
        divider = len(jogadores)
        if divider == 0:
            return True
        for jogador in jogadores:
            jogador.recebe(0, sala.valor // divider)
        sala.atualiza_saldo(divider)
        return True

    def entra(self, cena):
        cena.elt <= self.elt.elt

    def __eq__(self, carta):
        # print("carta.face == self.face", carta.face == self.face, carta.face, self.face)
        return carta.face == self.face


class Perigo(Carta):
    """
        Carta que representa um perigo, o aparecimento de duas encerra a rodada.

    """

    def termina(self, salas):
        return self in salas

    def divide(self, jogadores, salas):
        _ = jogadores
        return self not in salas


class Artefato(Carta):
    """
        Carta que representa um artefato, só pode ser recolhida quando um jogador sai sozinho.

    """

    def __init__(self, face):
        super().__init__(face)
        self.valor = 10  # // Carta.VALOR
        self.elt.mostra(":{}:".format(self.valor))

    def atualiza_saldo(self, divider):
        pass

    def divide_valor(self, jogadores, salas):
        if len(jogadores) == 1:
            jogadores[0].recebe(0, self.valor)
            self.valor = 0
            self.mostra()
        return True

    def mostra(self):
        self.elt.mostra(":{}:".format(self.valor))
        return True


class Tesouro(Carta):
    """
        Carta que representa um tesouro, O valor é dividido pelos jogadores ativos.

    """

    def __init__(self, face):
        super().__init__(face)
        self.elt.mostra(":{}:".format(self.valor))

    def premia(self, jogador, cota):
        jogador.recebe(self.valor // cota)
        # self.valor %= cota
        return True

    def mostra(self):
        self.elt.mostra(":{}:".format(self.valor))
        return True


class Baralho(object):
    """
        Contém as cartas a serem usadas nesta rodada.

    """
    def __init__(self):
        self.cartas = []
        self.monta_baralho()

    def embaralha(self, artefato):
        self.cartas.append(Artefato(face=artefato))
        [carta.inicia() for carta in self.cartas]
        shuffle(self.cartas)

    def descarta(self):
        return self.cartas.pop() if self.cartas else None

    def monta_baralho(self):
        self.cartas = []
        for perigo in PERIGOS * 3:
            self.cartas.append(Perigo(face=perigo))
        for tesouro in TESOUROS:
            self.cartas.append(Tesouro(face=tesouro))

    def extend(self, salas):
        self.cartas.extend(salas)


class Jogador(object):

    def __init__(self, mesa, jogador):
        """
            Representa um explorador, que pode ser um participante ou um NPC.

        :param jogador: módulo que contém a IA deste jogador.
        :param mesa: a mesa em que o jogador acampa.
        """
        self.sprite = Jogo.GUI.carta('decide', tit=jogador)
        self.tesouro = 0
        self.nome = jogador.nome
        self.mesa = mesa
        self.mesa.admite(self.sprite)
        self.jogador = jogador
        self.jogada, self.joias, self.mesa = None, 0, mesa
        self.mostra()

    def _inicia(self, jogador):
        try:
            exec(GET_JOGADOR.format(mod=jogador))
            self.nome = self.nome.upper()
            self.mostra()
        except (ModuleNotFoundError, TypeError):
            self.jogador = self

    def mostra(self):
        self.sprite.mostra("{}{}{}".format(self.tesouro, self.nome[:1], self.joias))

    def entra(self):
        self.joias = 0
        self.mostra()
        self.sprite.face(1)
        self.mesa.admite(self.sprite)

    def recebe(self, joias, tesouro=0):
        self.joias += joias
        self.tesouro += tesouro
        self.mostra()

    def decide(self):
        desiste = self.jogador.joga(self.mesa)
        if desiste:
            self.tesouro += self.joias
            self.joias = 0
            self.mostra()
            self.sprite.face(0)
        return desiste


class Mesa(object):
    """
        Contém o acampamento dos jogadores e apresenta as cartas da exploração em cada rodada.

    :param jogadores: Tuplas com a roleta e o nome do módulo do jogador
    """

    def __init__(self, jogadores):
        self.rodada_corrente = 0
        self.interval = None
        Jogo.GUI.splash()
        self.fases = Jogo.GUI.fases
        self.admite = Jogo.GUI.admite
        self.mesa = self.fases(self.rodada_corrente)
        self.baralho = Baralho()
        self.jogadores = [Jogador(self, jogador) for jogador in jogadores]
        self.jogadores_ativos = self.jogadores[:]
        self.jogadores_saindo = []
        self.perigo = self.salas = []
        self.perigos = self.artefatos = self.cartas = self.rodadas = self.jogadores_jogando = 0
        self.tesouros_na_mesa = self.tesouros_jogadores = self.cartas_na_mesa =\
            self.tesouros_na_tenda = self.joias_jogadores = []
        self.maior_tesouro = self.maior_joias = 0
        # self.inicia()

    def _cria_jogo(self, jogadores=JOGADORES):
        class JogadorSimples:
            def __init__(self, _, nome):
                _chance = list(range(20))
                shuffle(_chance)
                self.jogadas, self.nome = _chance, nome

            def joga(self, _):
                return (self.jogadas.pop() < 2) if self.jogadas else True

        return [JogadorSimples(*jogador) for jogador in jogadores]

    def atualiza(self, valores=True):
        if valores:
            return self.perigos, self.artefatos, self.cartas, self.rodada_corrente,\
                   self.maior_tesouro, self.maior_joias,\
                   self.jogadores_jogando, self.tesouros_na_tenda, self.cartas_na_mesa,\
                   self.tesouros_na_mesa, self.tesouros_jogadores, self.joias_jogadores

        self.perigos = sum(1 for carta in self.salas if isinstance(carta, Perigo))
        self.artefatos = sum(1 for carta in self.salas if isinstance(carta, Artefato))
        self.tesouros_jogadores = [jogador.tesouro for jogador in self.jogadores]
        self.joias_jogadores = [jogador.joias for jogador in self.jogadores_ativos]
        self.tesouros_na_tenda = [jogador.tesouro for jogador in self.jogadores]
        self.maior_tesouro = max(self.tesouros_na_tenda) if self.tesouros_na_tenda else 0
        self.maior_joias = max(self.joias_jogadores) if self.joias_jogadores else 0
        self.cartas, self.jogadores_jogando = len(self.salas), len(self.jogadores_ativos)
        self.tesouros_na_mesa = [carta.valor for carta in self.salas]
        self.cartas_na_mesa = [carta.face[:2] for carta in self.salas]

    def inicia(self):
        Jogo.GUI.set_timeout(self.rodada, 2000)
        # self.rodada(ARTEFATOS[0])

    def inicia_(self):
        self.mesa.vai()
        for artefato in ARTEFATOS:  # [:1]:
            self.baralho.extend([Artefato(artefato)])
        while self.baralho.cartas:
            self.apresenta(self.baralho.cartas.pop())

    def _inicia(self):
        self.mesa.vai()
        for _ in ARTEFATOS:  # [:1]:
            self.rodada()

    def rodada(self):
        if len(ARTEFATOS) <= self.rodada_corrente:
            return
        artefato = ARTEFATOS[self.rodada_corrente]
        self.mesa = self.fases(self.rodada_corrente)  # )
        self.mesa.vai()
        self.jogadores_ativos = self.jogadores[:]
        [jogador.entra() for jogador in self.jogadores]
        self.baralho.extend(self.salas)
        self.baralho.embaralha(artefato)
        self.perigo = self.salas = []
        self.interval = Jogo.GUI.set_interval(self.turno, 500)
        return

    def apresenta(self, carta):
        self.salas.append(carta)
        self.mesa.apresenta(carta)

    def turno(self):
        carta_corrente = self.baralho.descarta()
        if (not carta_corrente) or (carta_corrente.termina(self.salas)):
            self.mesa.apresenta(carta_corrente)
            Jogo.GUI.clear_interval(self.interval)
            if self.rodada_corrente <= 5:
                self.rodada_corrente += 1
                Jogo.GUI.set_timeout(self.rodada, 2000)
            return False
        self.jogadores_saindo = []
        self.apresenta(carta_corrente)
        ativos = len(self.jogadores_ativos)
        self.atualiza(False)
        for jogador in self.jogadores_ativos:
            for carta in self.salas:
                carta.premia(jogador, ativos)
            if jogador.decide() == DESISTE:
                self.jogadores_saindo.append(jogador)
        self.jogadores_ativos = [jogador for jogador in self.jogadores_ativos if jogador not in self.jogadores_saindo]
        carta_corrente.atualiza_saldo(ativos)
        carta_corrente.divide(self.jogadores_saindo, self.salas)
        if not self.jogadores_ativos:
            Jogo.GUI.clear_interval(self.interval)
            if self.rodada_corrente <= 5:
                self.rodada_corrente += 1
                Jogo.GUI.set_timeout(self.rodada, 2000)


class Jogo:
    GUI = None

    def __init__(self, jogadores=JOGADORES, gui=None):
        """
            O Jogo do Tesouro Inca.

        :param jogadores: vetor de tuplas com (roleta, nome do módulo)
        :param gui: Interface gráfica para apresentar o jogo.
        """
        Jogo.GUI = gui
        self.mesa = Mesa(jogadores)

    def inicia(self):
        self.mesa.inicia()
