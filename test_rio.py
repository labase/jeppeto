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

NENHURES = None

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
    def _inicia(self):
        self.local = NENHURES
        self.items =[]
        self.__recebe = self.recebe
    def recebe(self,elemento):
        elemento.move(self,self.x,self.y)
        self.recebe = self._nem_recebe
        return True
    def _nem_recebe(self,elemento):
        return False
    def registra(self,elemento,via):
        self.via = via
        self.recebe(elemento)
    def envia(self,elemento):
        self.via.envia(elemento)
    def devolve(self,elemento):
        self.items.remove(elemento)
        assert not self.items, 'items left! %s'%str(self.items)
        self.recebe= self.__recebe
    def move(self,local,x,y):
        pass
    def adentra(self,elemento):
        self.items.append(elemento)

class _PassagemNenhuma:#(Passagem):
    def devolve(self,elemento): pass
    def __call__(self):
        return self

NENHURES = _PassagemNenhuma()
del _PassagemNenhuma

class Porto(Passagem):
    def registra(self,elemento,via):
        self.via = via
        self.mestre = elemento
        self.mestre.move(self,self.x,self.y)
    def recebe(self,elemento):
        [item.recebe(elemento) for item in self.items]
    def envia(self,elemento):
        mestre = self.mestre
        elemento.move(mestre,mestre.x,mestre.y)
    def devolve(self,elemento):
        self.items.remove(elemento)
        self.via.apura()
      
class Passageiro(Local):
    def _inicia(self):
        self.local = NENHURES
        self.items =[]
        self.do_move = self.__no_move
    def entra(self,destino):
        destino.recebe(self)
        self.local.devolve(self)
    def age(self):
        self.do_move = self.move
        self.local.envia(self)
        self.do_move = self.__no_move
    def __no_move(self,local,x,y):
        pass
    def move(self,local,x,y):
        self.local.devolve(self)
        self.local = local
        self.local.adentra(self)
        dx, dy = x - self.x, y - self.y
        self.x, self.y = x,y
        [item.ajusta(dx,dy) for item in self.items]
    def ajusta(self,x,y):
        self.x += x
        self.y += y
    def devolve(self,elemento):
        pass
    def adentra(self,elemento):
        pass
    
class Lobo(Passageiro):pass
class Ovelha(Passageiro):pass
class Couve(Passageiro):pass

class Barco(Passageiro):#,Passagem):
    def recebe(self,elemento):
        elemento.move(self,self.x,self.y)
        self.items.append(elemento)
        self.__recebe, self.recebe= self.recebe, self._nem_recebe
    def _nem_recebe(self,elemento):
        pass
    def devolve(self,elemento):
        assert isinstance(elemento, Passageiro), 'Instead retrieved %s'%str(elemento)
        self.items.remove(elemento)
        self.recebe= self.__recebe
    def envia(self,elemento):
        self.local.via.recebe(elemento)
    pass
      
class Margem(Local):
    def _inicia(self):
        self.lobo = Passagem(self.x,100)
        self.ovelha = Passagem(self.x,200)
        self.couve = Passagem(self.x,300)
        self.lugares = (self.lobo,self.ovelha,self.couve)
    def apura(self):
        passageiros_nesta_margem = set([pas for lugar in self.lugares for pas in lugar.items ])
        if (passageiros_nesta_margem in Rio.AZAR):
            raise Exception, 'Desastre: %s'%str(passageiros_nesta_margem)
    def recebe(self,elemento):
        for lugar in self.lugares:
            if lugar.recebe(elemento): break
    def envia(self,elemento):
        self.via.recebe(elemento)
    def registra(self,elemento,via):
        self.via = via
        [lugar.registra(item,self) for lugar,item in zip(self.lugares,elemento)]

LOBO,OVELHA,COUVE = range(3)        
class Rio(Margem):
    AZAR=[]
    def _inicia(self):
        self.x = 100
        #p = self.passageiros = [Passageiro(),Passageiro(),Passageiro()]
        p = self.passageiros = [Lobo(),Ovelha(),Couve()]
        #Rio.AZAR = [set([p[LOBO],p[OVELHA],None]),set([p[COUVE],p[OVELHA],None])]
        Rio.AZAR = [set([p[LOBO],p[OVELHA]]),set([p[COUVE],p[OVELHA]])]
        self.ante_margem = Margem()
        self.margem = Margem(300)
        #[self.ante_margem.recebe(passageiro) for passageiro in self.passageiros]
        self.via = Barco(100)
        self.ante_pier, self.pier = self.lugares = [Porto(100),Porto(200)]
        self.ante_pier.registra(self.pier,self.ante_margem)
        self.pier.registra(self.ante_pier,self.margem)
        self.pier.envia(self.via)
        self.margem.registra(self.passageiros,self.pier)
        self.ante_margem.registra(self.passageiros,self.ante_pier)
    def recebe(self,elemento):
        self.via.recebe(elemento)

from mock import Mock

import unittest

class TestRio(unittest.TestCase):
    """can build the math stamp book"""
    def _main(self):
        #self.e = Mock(name= 'element')
        return None
    def setUp(self):
        self._main()
        self.r = Rio()
        self.lobo, self.ovelha, self.couve = self.r.passageiros
        self.barco = self.r.via
        self.cbarco = lambda:(self.barco.x,self.barco.y)
    
    def tearDown(self):
        #self.GUI.reset_mock()
        #self.mock.verify()
        #self.mock,MEMBER =None,None
        pass
    
    def test_animals_at_lef_margin(self):
        "os animais iniciam na margem esquerda"
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        locais = [passageiro.local for passageiro in self.r.passageiros]
        masters = (self.r.ante_pier.via,self.r.pier.via)
        margins = (self.r.ante_margem,self.r.margem)
        am ,pm = self.r.ante_margem, self.r.passageiros
        passageiros = set([pas for lugar in am.lugares for pas in lugar.items ])
        assert set(locais) == set(am.lugares), 'Instead passageiros were at %s but not at %s'%(str(locais),str(am.lugares))
        assert passageiros == set(pm), 'Instead passageiros were %s but at margins %s'%(str(passageiros),str(pm))
        assert masters == margins, 'Instead masters were %s but margins %s'%(str(masters),str(margins))
        assert all(isinstance(local, Passagem) for local in locais), 'Instead was %s'%str(locais)
        assert clobo[0]==covelha[0]==ccouve[0]==0, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert clobo[1]<>covelha[1]<>ccouve[1]<>clobo[1], 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
    def test_lamb_enters_ship_no_harm(self):
        "a ovelha entra no barco e ninguem se machuca"
        assert isinstance(self.r.via, Barco), 'Instead via was %s'%str(self.r.via)
        self.ovelha.age()
        self.lobo.age() #tenta entrar no barco e falha porque está cheio
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        am = self.r.ante_margem
        passageiros = set([pas for lugar in am.lugares for pas in lugar.items ])
        lobo_couve = self.r.passageiros[:]
        lobo_couve.remove(lobo_couve[1])
        assert self.ovelha.local == self.r.via, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert set(lobo_couve) == passageiros, 'passageiros not lobo couve but %s in %s'%(passageiros,lobo_couve)
        assert clobo[0]==ccouve[0]==0, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert covelha == (100,0), 'Instead ovelha was %s'%str(covelha)
    def test_boat_crosses_river_and_back(self):
        "o barco atravessa o rio e volta"
        assert self.r.ante_pier.x == 100, 'Instead ante_pier x was %s'%str(self.r.ante_pier.x)
        assert self.cbarco() == (100,0), 'Instead barco was %s'%str(self.cbarco())
        assert self.barco.local == self.r.ante_pier, 'Instead barco was at%s'%str(self.barco.local)
        self.barco.age()
        assert self.barco.local == self.r.pier, 'Instead barco was at%s'%str(self.barco.local)
        assert self.cbarco() == (200,0), 'Instead barco was %s'%str(self.cbarco())
        self.barco.age()
        assert self.barco.local == self.r.ante_pier, 'Barco not back, but stayed at%s'%str(self.barco.local)
        assert self.cbarco() == (100,0), 'Instead barco was %s'%str(self.cbarco())
    def test_lamb_cross_river_in_boat_but_fails_returning(self):
        "a ovelha atravessa o rio no barco e perde a viagem de volta"
        self.ovelha.age()
        self.barco.age()
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        assert self.barco.local == self.r.pier, 'Instead barco was at%s'%str(self.barco.local)
        assert self.barco in self.r.pier.items, 'Instead pier had %s'%str(self.r.pier.items)
        assert self.cbarco() == (200,0), 'Instead barco was %s'%str(self.cbarco())
        assert self.ovelha.local == self.r.via, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert self.ovelha in self.barco.items, 'Instead barco had %s'%str(self.barco.items)
        assert clobo[0]==ccouve[0]==0, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert covelha == (200,0), 'Instead ovelha was %s'%str(covelha)
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age() #tenta entrar no barco e falha pois o barco não está nesta margem
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        assert self.barco.local == self.r.ante_pier, 'Barco not back, but stayed at%s'%str(self.barco.local)
        assert self.ovelha.local in self.r.margem.lugares, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert clobo[0]==ccouve[0]==0, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert covelha[0] == 300, 'Instead ovelha was %s'%str(covelha)
    def test_wolf_cross_river_in_boat_causing_havoc(self):
        "o lobo atravessa o rio criando a maior confusao"
        self.lobo.age()
        amargem = self.r.ante_margem
        locais_margem = [amargem.ovelha,amargem.couve,amargem.lobo]
        persona_margem = [per for local in locais_margem for per in local.items]
        assert set(persona_margem) in Rio.AZAR, 'Instead lobo place had %s'%str(persona_margem)
        self.assertRaises(Exception,self.barco.age)
    def test_cabbage_cross_river_in_boat_causing_havoc(self):
        "a couve atravessa o rio criando a maior confusao"
        self.couve.age()
        self.assertRaises(Exception,self.barco.age)
    def test_lamb_cross_river_in_boat_causing_havoc(self):
        "a ovelha atravessa o rio criando a maior confusao"
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        self.barco.age()
        self.lobo.age()
        self.barco.age()
        self.lobo.age()
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        self.assertRaises(Exception,self.barco.age)
    def test_all_animals_cross_in_safety(self):
        "os animais atravessam em segurança"
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        self.barco.age()
        self.lobo.age()
        self.barco.age()
        self.lobo.age()
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        self.couve.age()
        self.barco.age()
        self.couve.age()
        self.barco.age()
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        self.barco.age()
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        assert clobo[0]==covelha[0]==ccouve[0]==300, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert clobo[1]<>covelha[1]<>ccouve[1]<>clobo[1], 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
    def test_cabbage_cross_later_in_boat_causing_havoc(self):
        "a couve atravessa depois criando a maior confusao"
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        locais_margem = [self.r.margem.ovelha,self.r.margem.couve,self.r.margem.lobo]
        persona_margem = [per for local in locais_margem for per in local.items]
        assert self.ovelha.local in locais_margem, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert self.ovelha in persona_margem, 'Instead ovelha place had first%s'%str(self.r.margem.ovelha.item)
        self.barco.age()
        self.couve.age()
        self.barco.age()
        self.couve.age()
        items, margem = [], self.r.margem
        margem_items = (margem.couve.items,margem.lobo.items,margem.ovelha.items)
        [items.extend(it) for it in margem_items]
        assert self.couve.local.via == self.r.margem, 'Instead couve was at%s'%str(self.couve.local)
        assert self.ovelha.local.via == self.r.margem, 'Instead couve was at%s'%str(self.couve.local)
        assert self.ovelha in items, 'Instead ovelha place had%s'%str(items)
        assert self.couve in items, 'Instead couve place had%s'%str(items)
        assert [] in margem_items, 'Instead margin itens where %s'%str(margem_items)
        self.assertRaises(Exception,self.barco.age)
'''
'''