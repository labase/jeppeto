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
    Módulo de teste da lógica central do jogo do Tesouro Inca.
.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
"""
from tesouro.tesouro import Jogo, Tesouro, Perigo, Artefato, TESOUROS, PERIGOS, ARTEFATOS
from unittest import TestCase, main
from unittest.mock import MagicMock
from random import shuffle
JOGADORES = tuple("roxanne libby sara kellee courtney angie naomi tracy morgan".split())


def _main(jogadores=JOGADORES, gui=None):
    class JogadorSimples:
        def __init__(self, joga, nome):
            _chance = list(range(20))
            shuffle(_chance)
            self.joga, self.jogadas, self.nome = joga, _chance, nome
            self._inicia(nome)

        def _inicia(self, jogador):
            get_joga = "from {mod}.main import {mod}; self.joga = {mod}()"
            try:
                exec(get_joga.format(mod=jogador))
                self.nome = self.nome.upper()
            except (ModuleNotFoundError, TypeError):
                self.joga = self._joga

        def _joga(self, _):
            return self.jogadas.pop() < 2
    # return [JogadorSimples(*jogador) for jogador in jogadores]

    return Jogo(gui=gui, jogadores=[JogadorSimples(None, jogador) for jogador in jogadores])


class TesteTesouro(TestCase):
    def setUp(self):
        self.gui = MagicMock("gui")
        self.gui.fases = MagicMock("fases")
        self.gui.carta = MagicMock("carta")
        self.gui.carta.return_value = self.gui.sprite = MagicMock("sprite")
        self.gui.sprite.mostra = MagicMock("mostra")
        self.gui.sprite.face = MagicMock("face")
        self.gui.mesa = MagicMock("mesa")
        self.gui.mesa.vai = MagicMock("vai")
        self.gui.mesa.apresenta = MagicMock("apresenta")
        self.gui.fases.return_value = self.gui.mesa
        self.gui.splash = MagicMock("splash")
        self.gui.set_timeout = MagicMock("timeout")
        self.gui.set_interval = MagicMock("set_interval")
        self.gui.clear_interval = MagicMock("set_interval")
        self.gui.admite = MagicMock("adimite")
        self._cria_jogo((([0], "pega_tesouro"), ))
        # self.jogo = Jogo(gui=self.gui)

    def test_turno(self):
        self._cria_jogo((([0, 0, 0, 0, 0, 0], "pega_tesouro"), ))
        mesa = self.jogo.mesa
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        # self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[i]) for i in range(5)]
        self.jogo.mesa.rodada()
        self.assertIn(Artefato("estatua"), self.jogo.mesa.baralho.cartas)
        # self._test_turno()
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        mesa.turno()
        # perigos,artef,cartas,rodada,maior_t,maior_j,jogadores,tenda,cartas,mesa,tesouros,joias
        #                 pe,ar,ca,ro,>t,>j,jg,tnd,crt,tnm,tsj,jsj
        self.assertEqual((0, 0, 1, 1, 0, 0, 1, [0], ['1'], [1], [0], [0]), mesa.atualiza(), mesa.atualiza())
        self.jogo.mesa.rodada()
        self.assertIn(Artefato(ARTEFATOS[1]), self.jogo.mesa.baralho.cartas)
        self.jogo.mesa.salas = []
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        mesa.turno()
        self.assertEqual((0, 0, 1, 2, 1, 0, 1, [1], ['1'], [1], [1], [0]), mesa.atualiza(), mesa.atualiza())
        self.jogo.mesa.rodada()
        self.assertIn(Artefato(ARTEFATOS[2]), self.jogo.mesa.baralho.cartas)
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        mesa.turno()
        self.assertEqual((0, 0, 1, 3, 2, 0, 1, [2], ['1'], [1], [2], [0]), mesa.atualiza(), mesa.atualiza())
        self.jogo.mesa.rodada()
        self.assertIn(Artefato(ARTEFATOS[3]), self.jogo.mesa.baralho.cartas)
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        mesa.turno()
        self.assertEqual((0, 0, 1, 4, 3, 0, 1, [3], ['1'], [1], [3], [0]), mesa.atualiza(), mesa.atualiza())
        self.jogo.mesa.rodada()
        self.assertIn(Artefato(ARTEFATOS[4]), self.jogo.mesa.baralho.cartas)
        self.jogo.mesa.baralho.cartas = [Tesouro(face=TESOUROS[0])]
        mesa.turno()
        self.assertEqual((0, 0, 1, 5, 4, 0, 1, [4], ['1'], [1], [4], [0]), mesa.atualiza(), mesa.atualiza())
        mesa.rodada()

    def _test_turno(self):
        self.jogo.mesa.turno()
        self.gui.mesa.apresenta.assert_called_once()
        self.gui.mesa.apresenta.reset_mock()
        # self.gui.set_timeout.assert_called_once()
        self.gui.set_timeout.reset_mock()
        # self.gui.set_interval.assert_called_once()
        # self.gui.clear_interval.assert_not_called()
        # self.gui.set_interval.reset_mock()

    def test_tesouro(self):
        self._cria_jogo((([0], "pega_tesouro"), ))
        mesa = self.jogo.mesa
        mesa.baralho.cartas = []
        mesa.baralho.cartas.append(Tesouro(face=TESOUROS[0]))
        mesa.turno()
        # perigos,artef,cartas,rodada,maior_t,maior_j,jogadores,tenda,cartas,mesa,tesouros,joias
        #                 pe,ar,ca,ro,>t,>j,jg,tnd,crt,tnm,tsj,jsj
        self.assertEqual((0, 0, 1, 1, 0, 0, 1, [0], ['1'], [1], [0], [0]), mesa.atualiza(), mesa.atualiza())
        mesa.atualiza(False)
        self.assertEqual((0, 0, 1, 1, 1, 0, 0, [1], ['1'], [0], [1], []), mesa.atualiza(), mesa.atualiza())
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(1, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(0, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(1, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(0, sai[0].joias, "Tesouro = {}".format(sai[0].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        # self.gui.sprite.mostra.assert_called_with(":10:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def _cria_jogo(self, jogadores=(([0], "pega_tesouro"), )):
        class Jogador:
            def __init__(self, jogadas, nome):
                self.jogadas, self.nome = jogadas, nome

            def joga(self, _):
                return self.jogadas.pop() < 2
        self.jogo = Jogo(gui=self.gui, jogadores=[Jogador(*jogador) for jogador in jogadores])

    def test_perigo(self):
        self._cria_jogo([([5, 5], "Perde1"), ([5, 5], "Perde2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Perigo(face=PERIGOS[4]))
        self.jogo.mesa.baralho.cartas.append(Perigo(face=PERIGOS[4]))
        self.jogo.mesa.turno()
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(2, len(ativos), "Ativos = {}".format(ativos))
        # self.assertEqual(0, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        # self.assertEqual(0, sai[0].joias, "Tesouro = {}".format(sai[0].joias))
        self.assertEqual(0, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.clear_interval.assert_called_once()

    def test_todos_saem_sem_artefato(self):
        self._cria_jogo([([0, 5], "todos_saem1"), ([0, 5], "todos_saem2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[3]))
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[2]))
        self.jogo.mesa.turno()
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(2, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(0, len(ativos), "Ativos = {}".format(ativos))
        # self.assertEqual(0, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(2, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        # self.assertEqual(0, sai[0].joias, "Tesouro = {}".format(sai[0].joias))
        # self.assertEqual(0, sai[0].joias, "Joias = {}".format(sai[0].joias))
        self.assertEqual(10, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.assertEqual(0, self.jogo.mesa.salas[1].valor, "Artefato = {}".format(self.jogo.mesa.salas[1].valor))
        self.gui.clear_interval.assert_called_once()

    def test_todos_saem(self):
        self._cria_jogo([([0, 5], "todos_saem1"), ([0, 5], "todos_saem2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[3]))
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[2]))
        self.jogo.mesa.turno()
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(1, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(1, ativos[1].joias, "Joias = {}".format(ativos[1].joias))
        self.assertEqual(1, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(2, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(0, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(3, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(3, sai[1].tesouro, "Tesouro = {}".format(sai[1].tesouro))
        self.assertEqual(1, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.assertEqual(0, self.jogo.mesa.salas[1].valor, "Tesouro = {}".format(self.jogo.mesa.salas[1].valor))
        self.gui.clear_interval.assert_called_once()

    def test_sai_um(self):
        self._cria_jogo([([5, 5, 5], "fica1"), ([0, 5, 5], "sai2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[0]))
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[1]))
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[2]))
        self.jogo.mesa.turno()
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, ativos[0].joias, "joias = {}".format(ativos[0].joias))
        self.assertEqual(0, ativos[1].joias, "Joias = {}".format(ativos[1].joias))
        self.assertEqual(10, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.jogo.mesa.turno()
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(1, ativos[0].joias, "joias = {}".format(ativos[0].joias))
        self.assertEqual(1, ativos[1].joias, "Joias = {}".format(ativos[1].joias))
        self.assertEqual(0, self.jogo.mesa.salas[1].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(1, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(1, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(1, ativos[0].joias, "Joias = {}".format(ativos[0].joias))
        self.assertEqual(0, sai[0].joias, "Joias = {}".format(sai[0].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.assertEqual(0, self.jogo.mesa.salas[1].valor, "Tesouro = {}".format(self.jogo.mesa.salas[1].valor))
        self.assertEqual(0, self.jogo.mesa.salas[2].valor, "Artefato = {}".format(self.jogo.mesa.salas[2].valor))
        self.assertEqual(12, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        # self.gui.clear_interval.assert_called_once()

    def test_artefato_tesouro(self):
        self._cria_jogo([([0, 5], "pega_tesouro_artefato1"), ([5, 5], "pega_tesouro2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[4]))
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[4]))
        self.jogo.mesa.turno()
        self.gui.sprite.mostra.assert_called_with(":1:")
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(1, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(1, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(13, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(0, sai[0].joias, "Tesouro = {}".format(sai[0].joias))
        self.assertEqual(2, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.sprite.mostra.assert_called_with(":0:")

    def test_divide_tesouro(self):
        self._cria_jogo([([0], "pega_tesouro1"), ([0], "pega_tesouro2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[4]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(2, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(0, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(2, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(2, sai[1].tesouro, "Tesouro = {}".format(sai[1].tesouro))
        self.assertEqual(0, sai[0].joias, "Tesouro = {}".format(sai[0].joias))
        self.assertEqual(1, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        # self.gui.sprite.mostra.assert_called_with(":10:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_joia(self):
        self._cria_jogo([([5], "pega_joia")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(1, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(1, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        # self.gui.sprite.mostra.assert_called_with(":10:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_nao_pega_joia(self):
        self._cria_jogo([([5], "nao_pega_joia1"), ([5], "nao_pega_joia2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(2, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(0, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(1, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.sprite.mostra.assert_called_with(":1:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_divide_joia(self):
        self._cria_jogo([([5], "pega_joia1"), ([5], "pega_joia2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[1]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(2, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(1, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(1, ativos[1].joias, "Tesouro = {}".format(ativos[1].joias))
        self.assertEqual(0, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.sprite.mostra.assert_called_with(":0:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_divide_e_fica_joia(self):
        self._cria_jogo([([5], "pega_joia1"), ([5], "pega_joia2")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Tesouro(face=TESOUROS[2]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(2, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.assertEqual(1, ativos[0].joias, "Tesouro = {}".format(ativos[0].joias))
        self.assertEqual(1, ativos[1].joias, "Tesouro = {}".format(ativos[1].joias))
        self.assertEqual(1, self.jogo.mesa.salas[0].valor, "Tesouro = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.sprite.mostra.assert_called_with(":1:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_artefato_nao_pego(self):
        self._cria_jogo([([5], "nao_pega_artefato")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        ativos = self.jogo.mesa.jogadores_ativos
        self.assertEqual(0, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(1, len(ativos), "Ativos = {}".format(ativos))
        self.assertEqual(0, ativos[0].tesouro, "Tesouro = {}".format(ativos[0].tesouro))
        self.gui.sprite.mostra.assert_called_with(":10:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_artefato_pego(self):
        self._cria_jogo([([0], "pega_artefato")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        self.assertEqual(1, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(10, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.gui.sprite.mostra.assert_called_with(":0:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_artefato_nao_disputado(self):
        self._cria_jogo([([5], "sai_nd"), ([0], "fica_nd")])
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        self.assertEqual(1, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(10, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.gui.sprite.mostra.assert_called_with(":0:")
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_artefato_disputado(self):
        self._cria_jogo([([0], "sai_a"), ([0], "sai_b")])
        self.assertEqual(2, len(self.jogo.mesa.jogadores),
                         "jogadores registrados = {}".format(len(self.jogo.mesa.jogadores)))
        self.jogo.mesa.baralho.cartas = []
        self.jogo.mesa.baralho.cartas.append(Artefato(face=ARTEFATOS[0]))
        self.jogo.mesa.turno()
        sai = self.jogo.mesa.jogadores_saindo
        self.assertEqual(2, len(sai), "Saindo = {}".format(sai))
        self.assertEqual(0, sai[0].tesouro, "Tesouro = {}".format(sai[0].tesouro))
        self.assertEqual(0, sai[1].tesouro, "Tesouro = {}".format(sai[1].tesouro))
        self.assertEqual(10, self.jogo.mesa.salas[0].valor, "Artefato = {}".format(self.jogo.mesa.salas[0].valor))
        self.gui.mesa.apresenta.assert_called_once()
        # self.gui.set_timeout.assert_called_once()

    def test_rodada(self):
        self.jogo.mesa.rodada()
        # self.gui.fases.assert_called_once_with(0)
        assert 2 == self.gui.admite.call_count, self.gui.admite.call_count
        self.gui.set_interval.assert_called_once()

    def test_inicia(self):
        self.jogo.inicia()
        self.gui.splash.assert_called_once()
        self.gui.fases.assert_called_once()
        self.gui.fases.assert_called_once_with(0)
        # assert 36 == self.gui.carta.call_count
        assert 1 == self.gui.admite.call_count, self.gui.admite.call_count
        self.gui.set_timeout.assert_called_once()
        self.gui.sprite.mostra.assert_called_with('0p0')

    def test_main(self):
        self.jogo = _main(gui=self.gui)
        self.jogo.inicia()
        self.gui.fases.assert_called_with(0)
        assert 10 == self.gui.admite.call_count, self.gui.admite.call_count
        self.gui.set_timeout.assert_called_once()
        self.gui.sprite.mostra.assert_called_with('0m0')


if __name__ == '__main__':
    main()
    # Jogo().inicia()
