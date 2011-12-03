#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : An Educational Game Builder
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/12/02  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/12/02 $Date$"

class Elemento:
    """ Um elemento básico do Jogo.
    """
    TEMPO = 0
    def __init__(self, x=0, y=0, imagem = None):
        """ inicia a posição e a imagem
        """
        self.x, self.y = x, y
        self.imagem = imagem or self
        self._inicia()
    def _inicia(self):
        pass
       
class Local(Elemento):
    """ Um local onde se pode colocar Elementos
    """
    def _inicia(self):
        pass

class Atividade(Elemento):
    """ Um comportamento que pode ser atribuido a um elemento ou local
    """
    def _inicia(self):
        pass
class Passagem(Local):
    def recebe(self,elemento):
        self.mestre.move(self,self.x,self.y)
    def registra(self,elemento,via):
        self.via = via
        self.mestre = elemento
    def envia(self,elemento):
        self.via.envia(elemento)
    def devolve(self,elemento):
        pass
class LocalLobo(Passagem):
    pass
class LocalOvelha(Passagem):
    pass
class LocalCouve(Passagem):
    pass
class LocalBarco(Passagem):
    pass
      
class Passageiro(Local):
    def _inicia(self):
        self.local = self
    def entra(self,destino):
        destino.recebe(self)
        self.local.devolve(self)
    def age(self):
        self.local.envia(self)
    def move(self,local,x,y):
        self.local = local
        self.local.devolve(self)
        self.x, self.y = x,y
    def sai(self,item):
        pass
class Lobo(Passageiro):
    pass
class Ovelha(Passageiro):
    pass
class Couve(Passageiro):
    pass
class Barco(Passageiro,Passagem):
    def recebe(self,elemento):
        elemento.move(self,self.x,self.y)
    pass
      
class Margem(Local):
    def _inicia(self):
        self.lobo = LocalLobo(self.x,100)
        self.ovelha = LocalOvelha(self.x,200)
        self.couve = LocalCouve(self.x,300)
        self.barco = LocalBarco(self.x,400)
        self.lugares = (self.lobo,self.ovelha,self.couve)
    def recebe(self,elemento):
        [lugar.recebe(elemento) for lugar in self.lugares]
    def envia(self,elemento):
        self.via.recebe(elemento)
    def registra(self,elemento,via):
        self.via = via
        lugares = (self.lobo,self.ovelha,self.couve)
        [lugar.registra(item,self) for lugar,item in zip(lugares,elemento)]
        
class Rio(Margem):
    def _inicia(self):
        self.x = 100
        self.passageiros = [Lobo(),Couve(),Ovelha()]
        self.ante_margem = Margem()
        self.margem = Margem(300)
        self.via = Barco(100)
        self.margem.registra(self.passageiros,self)
        self.ante_margem.registra(self.passageiros,self)
        [self.ante_margem.recebe(passageiro) for passageiro in self.passageiros]
        self.lugares = [self.via]

from mock import Mock

import unittest

class TestRio(unittest.TestCase):
    """can build the math stamp book"""
    def _main(self):
        self.e = Mock(name= 'element')
        return None
    def setUp(self):
        self._main()
        self.r = Rio()
    
    def tearDown(self):
        #self.GUI.reset_mock()
        #self.mock.verify()
        #self.mock,MEMBER =None,None
        pass
    
    def test_animals_at_lef_margin(self):
        "os animais iniciam na margem esquerda"
        clobo, ccouve, covelha = [(p.x,p.y) for p in self.r.passageiros]
        assert clobo == (0,100), 'Instead was %s'%str(clobo)
        assert ccouve == (0,200), 'Instead was %s'%str(clobo)
        assert covelha == (0,300), 'Instead was %s'%str(clobo)
        #assert self.GUI.method_calls == [], 'Instead was %s'%self.GUI.method_calls
    def test_lamb_enters_ship_no_harm(self):
        "a ovelha entra no barco e ninguem se machuca"
        lobo, couve, ovelha = self.r.passageiros
        ovelha.age()
        clobo, ccouve, covelha = [(p.x,p.y) for p in self.r.passageiros]
        assert ovelha.local == self.r.via, 'Instead ovelha was at%s'%str(ovelha.local)
        assert clobo == (0,100), 'Instead lobo was %s'%str(clobo)
        assert ccouve == (0,200), 'Instead couve was %s'%str(clobo)
        assert covelha == (100,0), 'Instead ovelha was %s'%str(covelha)
