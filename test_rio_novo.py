#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : Jogo do Rio - Lobo - Cordeiro - Couve
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

NENHUM = NENHURES = None
class Elemento(list):
    """ Um elemento básico do Jogo, que tem uma lista de itens.
    """
    TEMPO = 0
    def __init__(self, x=0, y=0):
        """ inicia a posição e a imagem
        """
        #self.x, self.y = x, y
        self._inicia()
        self.local = NENHURES
        self.item = NENHUM
    def _inicia(self):
        """ inicia as características do elemento
        """
        pass      
    def entra(self,destino):
        """ O elemento entra em um destino
        """
        pass      
    def age(self):
        """ O elemento executa uma ação
        """
        pass
    def move(self,local):
        """ O elemento troca de lugar
        """
        pass
    def ajusta(self):
        pass
    def ativa():
        """ O elemento é ativado por uma ação
        """
        pass
class Lugar(Elemento):
    """ Um lugar básico do Jogo, que tem uma lista de itens.
    """
    def recebe(self,elemento):
        """ O lugar recebe um elemento
        """
        pass
    def envia(self,elemento):
        """ O lugar transporta o elemento para outro lugar
        """
        pass
    def devolve(self,elemento):
        """ O lugar devolve um elemento que estava nele
        """
        pass
    def aloca(self,elemento):
        pass
    def remove(self,elemento):
        pass
NENHURES = type('_Nenhures',(Lugar),dict(__call__ = lambda self: self))
del _Nenhures
NENHUM = type('_Nenhum',(Lugar),dict(__call__ = lambda self: self))
del _Nenhum
class Movente(list):
    """ Um elemento capaz de ser movimentado no jogo.
    """
    def _inicia(self):
        pass
    def entra(self,destino):
        self.local.devolve(self, lambda self:destino.recebe(self))       
    def age(self):
        self.item.ativa()
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
        self.item = elemento
        self.via = via
        self.mestre = elemento
        self.mestre.move(self,self.x,self.y)
    def envia(self,elemento):
        self.via.envia(elemento)
    def devolve(self,elemento):
        self.item = None
        pass
    def move(self,local,x,y):
        pass
    def adentra(self,elemento):
        self.item = elemento
        pass
class _PassagemNenhuma(Passagem):
    def __call__(self):
        return self

NENHURES = _PassagemNenhuma()
del _PassagemNenhuma

class Porto(Passagem):
    def _inicia(self):
        self.items = []
    def recebe(self,elemento):
        [item.recebe(elemento) for item in self.items]
    def envia(self,elemento):
        mestre = self.mestre
        elemento.move(mestre,mestre.x,mestre.y)
    def devolve(self,elemento):
        self.items.remove(elemento)
        self.via.apura()
    def adentra(self,elemento):
        self.items.append(elemento)
      
class Passageiro(Local):
    def _inicia(self):
        self.local = NENHURES
        self.items =[]
        #self._move, self.move = self.move, self._no_move
        self._move = self.move
    def entra(self,destino):
        destino.recebe(self)
        self.local.devolve(self)
    def age(self):
        self.move = self._move
        self.local.envia(self)
        self.move = self._no_move
    def _no_move(self,local,x,y):
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
    #def sai(self,item):
    #    pass
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
    def age(self):
        self.local.envia(self)
    pass
      
class Margem(Local):
    def _inicia(self):
        self.lobo = Passagem(self.x,100)
        self.ovelha = Passagem(self.x,200)
        self.couve = Passagem(self.x,300)
        self.lugares = (self.lobo,self.ovelha,self.couve)
    def apura(self):
        passageiros_nesta_margem = set([lugar.item for lugar in self.lugares])
        if (passageiros_nesta_margem in Rio.AZAR):
            raise Exception, 'Desastre: %s'%str(passageiros_nesta_margem)
    def recebe(self,elemento):
        [lugar.recebe(elemento) for lugar in self.lugares]
    def envia(self,elemento):
        self.via.recebe(elemento)
    def registra(self,elemento,via):
        self.via = via
        lugares = (self.lobo,self.ovelha,self.couve)
        [lugar.registra(item,self) for lugar,item in zip(lugares,elemento)]
LOBO,OVELHA,COUVE = range(3)        
class Rio(Margem):
    AZAR=[]
    def _inicia(self):
        self.x = 100
        #p = self.passageiros = [Passageiro(),Passageiro(),Passageiro()]
        p = self.passageiros = [Lobo(),Ovelha(),Couve()]
        Rio.AZAR = [set([p[LOBO],p[OVELHA],None]),set([p[COUVE],p[OVELHA],None])]
        self.ante_margem = Margem()
        self.margem = Margem(300)
        self.via = Barco(100)
        self.ante_pier, self.pier = self.lugares = [Porto(100),Porto(200)]
        self.ante_pier.registra(self.pier,self.ante_margem)
        self.pier.registra(self.ante_pier,self.margem)
        self.pier.envia(self.via)
        self.margem.registra(self.passageiros,self.pier)
        self.ante_margem.registra(self.passageiros,self.ante_pier)
    def recebe(self,elemento):
        self.via.recebe(elemento)
'''
from mock import Mock
'''
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
        assert masters == margins, 'Instead masters were %s but margins %s'%(str(masters),str(margins))
        assert all(isinstance(local, Passagem) for local in locais), 'Instead was %s'%str(locais)
        assert clobo[0]==covelha[0]==ccouve[0]==0, 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
        assert clobo[1]<>covelha[1]<>ccouve[1]<>clobo[1], 'Instead was %s'%str(clobo)+str(covelha)+str(ccouve)
    def test_lamb_enters_ship_no_harm(self):
        "a ovelha entra no barco e ninguem se machuca"
        assert isinstance(self.r.via, Barco), 'Instead via was %s'%str(self.r.via)
        self.ovelha.age()
        #self.lobo.age() #tenta entrar no barco e falha porque está cheio
        clobo, covelha, ccouve = [(p.x,p.y) for p in self.r.passageiros]
        am = self.r.ante_margem
        passageiros = [set([l.item for l in am.lugares])]
        lobo_couve =  set([am.lobo.item,am.ovelha.item,am.couve.item])
        assert self.ovelha.local == self.r.via, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert lobo_couve in passageiros, 'passageiros not lobo couve but %s in %s'%(passageiros,lobo_couve)
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
'''
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
        assert covelha == (300,200), 'Instead ovelha was %s'%str(covelha)
    def test_wolf_cross_river_in_boat_causing_havoc(self):
        "o lobo atravessa o rio criando a maior confusao"
        self.lobo.age()
        #self.barco.age()
        self.assertRaises(Exception,self.barco.age)
    def test_cabbage_cross_river_in_boat_causing_havoc(self):
        "a couve atravessa o rio criando a maior confusao"
        self.couve.age()
        #self.barco.age()
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
        #self.assertRaises(Exception,self.barco.age)
    def test_cabbage_cross_later_in_boat_causing_havoc(self):
        "a couve atravessa depois criando a maior confusao"
        self.ovelha.age()
        self.barco.age()
        self.ovelha.age()
        assert self.ovelha.local == self.r.margem.ovelha, 'Instead ovelha was at%s'%str(self.ovelha.local)
        assert self.ovelha == self.r.margem.ovelha.item, 'Instead ovelha place had first%s'%str(self.r.margem.ovelha.item)
        assert None == self.r.margem.lobo.item, 'Instead lobo place had %s'%str(self.r.margem.lobo.item)
        self.barco.age()
        self.couve.age()
        self.barco.age()
        self.couve.age()
        assert self.couve.local == self.r.margem.couve, 'Instead ovelha was at%s'%str(self.couve.local)
        assert self.ovelha == self.r.margem.ovelha.item, 'Instead ovelha place had%s'%str(self.r.margem.ovelha.item)
        assert None == self.r.margem.lobo.item, 'Instead lobo place had %s'%str(self.r.margem.lobo.item)
        self.assertRaises(Exception,self.barco.age)
'''