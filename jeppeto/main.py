#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/12/12  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/12/12 $Date$"

from gui_decorator import Item, DragDecorator, DropDecorator

PRIMESXYZ = (5,11,111)
SATURATE = 256

HEX6 = '#%06x'
BLACK, WHITE , GREY , NAVWHITE ='#000000', '#FFFFFF', '#A0A0A0', '#FFDFB0'
BLOCK_SIZE = 50
BP = BLOCK_PADDING = 10
X,Y = (0,1)

class _Nenhures:
    """ Um elemento básico do Jogo.
    """
    TEMPO = 0
    def age(self,*args):
        return False
    def reage(self,*args):
        return False
    def ativa(self,ato):
        return False
    def entra(self,ato):
        return False
    def move(self,local):
        pass
    def adentra(self,local):
        return False
        pass
    def recebe(self,elemento):
        return False
    def devolve(self,elemento):
        return self
    def nada_faz(self, *args):
        pass
    def __call__(self):
        return self

NENHURES = _Nenhures()
del _Nenhures
       
class Elemento:
    """ Um elemento básico do Jogo.
    """
    TEMPO = 0
    def __init__(self, inicial =[]):
        """ inicia a posição e a imagem
        """
        self.local = NENHURES()
        self.items =[]
        self.agir = self.move
    def age(self,ato):
        self._age, self.age = self.age, self.nada_faz
        for item in self.items:
            if item.reage(ato or self.agir):
                self.age = self._age
                return True
        did = self.local.reage(ato or self.agir)
        self.age = self._age
        return did
    def _ativa(self,ato):
        return ato(self)
    def entra(self,ato):
        return ato(self)
    def reage(self,ato):
        return self.local.reage(ato)
    def move(self,local):
        return local.recebe(self, self.local.devolve)
    def ativa(self,ato):
        print 'nao ativa'
        return False
    def adentra(self,local):
        self.local = local
        return True
    def recebe(self, elemento, ato):
        if not elemento in self.items:
            self.items.append(elemento)
            ato(elemento)
            return elemento.adentra(self)
        return False
    def devolve(self,elemento):
        self.items.remove(elemento)
        return elemento
    def nada_faz(self, *args):
        return False

class Local(Elemento):
    """ Um local onde se pode colocar Elementos
    """
    def reage(self,ato):
        for item in self.items:
            if item.age(ato):
                return True
        did = self.local.age(ato or self.agir)
        return did
    def age(self,ato):
        print 'local age'
        #for item in self.items:
        #    if item.ativa(ato):
        #        return True
        return ato(self)
    def ativa(self,ato):
        print 'ativou'
    def entra(self,ato):
        for item in self.items:
            if item.entra(ato):
                return True
        #did = self.local.age(ato or self.agir)
        #return did

class Portal(Local):
    """ Um portal de passagens entre locais
    """
    def age(self,ato):
        return False
    def _age(self,ato):
        for item in self.items:
            if item.ativa(ato):
                return True
        else:
            return self.local.ativa(ato)
            return False
    def ativa(self,ato):
        print 'Portal ativou'
        for item in self.items:
            if item.entra(ato):
                return True
        did = self.local.entra(ato or self.agir)
        return did
       
class Referencia:
    """ Referencia Um elemento básico do Jogo.
    """
    def __init__(self, elemento):
        """ inicia o elemento de referência
        """
        self.elemento = elemento
    def entra(self,ato):
        return self.elemento.entra(ato)
    def age(self,ato):
        return self.elemento.age(ato)
    def ativa(self,ato):
        return self.elemento.ativa(ato)
    def reage(self,ato):
        return self.elemento.reage(ato)
    def move(self,local):
        return self.elemento.move(local)
    def adentra(self,local):
        return self.elemento.adentra(local)
    def recebe(self, elemento, ato):
        return self.elemento.recebe(elemento, ato)
    def devolve(self,elemento):
        return self.elemento.devolve(elemento)
       

class Atividade(Elemento):
    """ Um comportamento que pode ser atribuido a um elemento ou local
    """
    def _inicia(self):
        pass

class BlockItem(Item):
    """ Um bloco que arrasta e solta
    """
    def create(self):
        self.xy = self.origin = (0,0)
        self.size = (BLOCK_SIZE,BLOCK_SIZE)
        self.items =[]
        self.element = Elemento()
        return self.icon
    def _noaction(self,*args):
        return False
    def translate(self,dx,dy):
        self.avatar.translate(dx,dy)
        self.xy = self.icon.pos()
        [item.translate(dx,dy) for item in self.items]
    def revert(self):
        self._move(*self.origin)
        [item.revert() for item in self.items]
    def _start(self,x,y):
        self.origin = self.xy = self.avatar.pos()
        self.icon.toFront() # ZOrder not working in pygame!
        #self.icon.translatez(0,1000)
        #self.icon.translate(*self.origin)
        [item._start(x,y) for item in self.items]
        return True
    def _move(self,x,y):
        dx, dy = x - self.xy[X], y - self.xy[Y]
        self.translate(dx, dy)

    def delete(self):
        [item.delete() for item in self.items]
        self.container.remove(self)
        self.gui.unclick(self)
        self.gui.undrop(self)
        self.gui.undrag(self)
        self.avatar.remove()
        del self
    def remove(self,item):
        self.items.remove(item)
        return True
    def reshape(self,block):
        x,y = self.xy
        w,h = self.size
        ax, ay = (max([i.xy[X]+i.size[X]+BP for i in self.items+[block]]+[x]),
                   max([i.xy[Y]+i.size[Y]+BP for i in self.items+[block]]+[y]))
        nx, ny = (min([i.xy[X]-BP for i in self.items]+[x,block.xy[X]]),
                   min([i.xy[Y]-BP for i in self.items]+[y,block.xy[Y]]))
        self.size = (ax-nx, ay-ny)
        self.xy = (nx,ny)
        self.avatar.scale(*self.size)
        self.avatar.move(*self.xy)
        self.container.reshape(self)
        
class Composite(BlockItem):
    """ Um item composto
    """
    def _click(self,x,y):
        self.origin = self.xy
        self._create(x,y)
    def _create(self,x,y, comp = None):
        comp = comp or self.spawn(x,y,self._colour(x,y))
        self.items.append(comp)
        print 'paste %s'%self.items
        comp.local = self
        self.reshape(comp)
    def paste(self,x,y,item):
        if item is self:
            return False
        if not item in self.items:
            item.revert()
            self._create(x,y,comp = item.clone(x,y, owner = self))
            pass
        else:
            self.reshape(item)
        return True
        
    def _colour(self,x,y):
        xyz = zip ((x,y,x*y), PRIMESXYZ, (2,1,0))
        return sum((ord * prime) % SATURATE * SATURATE**axis
            for ord, prime, axis in xyz)
    def spawn(self,x,y, color= None, owner = None):
        color = color or self.clone_contents(x,y)
        comp = self.factory(self.stereotype(x,y,color), owner)
        return self._spawn(x,y,comp,color)
    def _spawn(self,x,y,comp,color):
        DragDecorator(comp,action=comp._move,start=comp._start,stop=comp.paste)
        DropDecorator(comp,comp.paste)
        comp.origin, comp.xy, comp.size = (x,y), (x,y),(BLOCK_SIZE,)* 2
        comp.color = color
        comp.icon.toFront()
        print 'spawned : %s'%color
        return comp
    def clone(self,x,y,color=None, owner = None):
        color = color or self.clone_contents(x,y)
        comp = Reference(self,self.stereotype(x,y,color), owner)
        return self._spawn(x,y,comp,color)
    def clone_contents(self,x,y):
        return self._colour(x,y)
    def factory(self, icon, owner = None):
        return Composite(self.gui,owner or self,icon)

    def stereotype(self,x,y,color):
        icon = self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = HEX6%color)
        self.gui.rect(0,0,BLOCK_SIZE,2,hexcolor=BLACK,buff=icon.image)
        return icon

class Locus(Composite,Local):
    """ Portal
    """
    def stereotype(self,x,y,color):
        icon =  self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = HEX6%color)
        self.gui.rect(0,0,BLOCK_SIZE,2,hexcolor=BLACK,buff=icon.image)
        return  icon
    def factory(self, icon, owner = None):
        return Locus(self.gui,owner or self,icon)

    def clone_contents(self,x,y):
        return self.color or self._colour(x,y)
    def recebe(self, elemento, ato):
        go = Local.recebe(self, elemento, ato)
        if go:
            x, y = self.icon.pos()
            elemento.icon.toFront()
            elemento._move(x+BP,y+BP)
            elemento.container = self
            self.reshape(elemento)
        return go
class Actor(Composite, Elemento):
    """ Actor
    """
    def recebe(self, elemento, ato):
        go = Elemento.recebe(self, elemento, ato)
        if go:
            x, y = self.icon.pos()
            elemento.icon.toFront()
            elemento._move(x+BP,y+BP)
            elemento.container = self
            self.reshape(elemento)
        return go
    def create(self):
        Elemento.__init__(self)
        return Composite.create(self)
    def stereotype(self,x,y,color):
        #color = 0xAAAAFF
        BLOCK = BLOCK_SIZE
        icon = self.gui.image(
            None, x, y, BLOCK, BLOCK, cl = HEX6%color)
        self.gui.rect(0,BLOCK-2,BLOCK_SIZE,2,hexcolor=BLACK,buff=icon.image)
        self.gui.rect(BLOCK//3,BLOCK-4,BLOCK//3,2,
                      hexcolor=BLACK,buff=icon.image)
        return  icon
    def factory(self, icon, owner = None):
        return Actor(self.gui,owner or self,icon)
    def _click(self,x,y):
        self.age(None)
        pass
    def clone_contents(self,x,y):
        return self.color or self._colour(x,y)
    #def adentrar(self, local): >>>> Remover?? sem problemas?
    #    self.local = local
    #    return True

class Port(Actor,Portal):
    """ Portal
    """
    def ativa(self,ato):
        return Portal.ativa(self,ato)
    def stereotype(self,x,y,color):
        icon = self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = HEX6%color)
        self.gui.rect(0,0,2,BLOCK_SIZE,hexcolor=BLACK,buff=icon.image)
        return  icon
    def factory(self, icon, owner = None):
        return Port(self.gui,owner or self,icon)
    

class Reference(Composite,Referencia):
    """ Portal
    """
    def __init__(self, referee, icon, owner):
        self.referee = referee
        Referencia.__init__(self,referee)
        Composite.__init__(self,referee.gui,owner,icon)
        self.gui.rect(0,0,4,4,hexcolor=BLACK,buff=self.icon.image)
        self.gui.rect(1,1,2,2,hexcolor=WHITE,buff=self.icon.image)
    def stereotype(self,x,y,color):
        icon = self.referee.stereotype(x,y,self.referee.color)
        self.gui.rect(0,0,4,4,hexcolor=WHITE,buff=icon.image)
        return icon
    def clone(self,x,y,color=None, owner = None):
        ref = self.referee
        color = ref.color
        comp = Reference(ref,ref.stereotype(x,y,color), owner)
        return self._spawn(x,y,comp,color)
    def adentra(self,local):
        pass
    
class Tool():
    """ Tool
    """
    def paste(self,x,y,item):
        item.revert()
    def delete(self):pass
    def clone(self,x,y,color=None, owner = None):
        return self.spawn(x,y,color,owner = owner)
    
class ToolActor(Tool,Actor):
    """ Ferramenta de Portal
    """
    def create(self):
        Actor.create(self)
        DragDecorator(self,action=self._move,start=self._start,stop=self.paste)
        self.colorz = 0xFFAAAA
        self.color = None
        BLOCK = BLOCK_SIZE-10
        self.icon = self.gui.image(
            None, 750, 200, BLOCK, BLOCK, cl = HEX6%self.colorz)
        self.gui.rect(0,BLOCK-1,BLOCK_SIZE,2,hexcolor=BLACK,buff=self.icon.image)
        self.gui.rect(BLOCK//3,BLOCK-2,BLOCK//3,2,
                      hexcolor=BLACK,buff=self.icon.image)
        self.xy = self.origin = (0,0)
        self.size = (BLOCK,BLOCK)
        self.items =[]
        return self.icon
    
class ToolPort(Tool,Port):
    """ Ferramenta de Portal
    """
    def create(self):
        Port.create(self)
        DragDecorator(self,action=self._move,start=self._start,stop=self.paste)
        self.colorz = 0xAAAAFF
        self.color = None
        BLOCK = BLOCK_SIZE-10
        self.icon = self.gui.image(
            None, 750, 250, BLOCK, BLOCK, cl = HEX6%self.colorz)
        self.gui.rect(0,0,2,BLOCK_SIZE,hexcolor=BLACK,buff=self.icon.image)
        self.xy = self.origin = (0,0)
        self.size = (BLOCK,BLOCK)
        self.items =[]
        return self.icon
    

class ToolLocus(Tool,Locus):
    """ Ferramenta de Locus
    """
    def create(self):
        DragDecorator(self,action=self._move,start=self._start,stop=self.paste)
        self.color = 0xFFAAAA
        self.icon = self.gui.image(
            None, 750, 200, BLOCK_SIZE-10, BLOCK_SIZE-10, cl = HEX6%self.color)
        self.gui.rect(0,0,2,BLOCK_SIZE,hexcolor=BLACK,buff=self.icon.image)
        self.items =[]
        return self.icon

class DustBin(Composite):
    """ Lata de lixo
    """
    def create(self):
        RR=3
        DropDecorator(self, self.scrap)
        self.icon = self.gui.image(
            None, 750, 430, BLOCK_SIZE-10, BLOCK_SIZE-10, cl = NAVWHITE)
        self.gui.rect(10,0,20,RR,hexcolor=GREY,buff=self.icon.image)
        self.gui.rect(2,RR,BLOCK_SIZE-14,BLOCK_SIZE-14,hexcolor=GREY,buff=self.icon.image)
        self.gui.rect(RR+8,RR+4,2,BLOCK_SIZE-24,hexcolor=NAVWHITE,buff=self.icon.image)
        self.gui.rect(RR+16,RR+4,2,BLOCK_SIZE-24,hexcolor=NAVWHITE,buff=self.icon.image)
        self.gui.rect(RR+24,RR+4,2,BLOCK_SIZE-24,hexcolor=NAVWHITE,buff=self.icon.image)
        self.gui.rect(0,RR+4,BLOCK_SIZE,2,hexcolor=NAVWHITE,buff=self.icon.image)
        self.gui.unclick(self)
        return self.icon
    def scrap(self,x,y,item):
        print "scrapping %s"%item
        item.delete()
        return True

class App(Locus):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        self.items =[]
        self.container = self
        self.color = None #0xFFDFBF
        self.xy = self.origin = (0,0)
        app = self.gui.text(350, 10, 'Jeppeto', hexcolor = '#FFDFBF')
        self.icon = app = self.gui.image( None,0, 0, 750, 600, cl = '#FFDFB6')
        self.activate = self._click
        comp = DustBin(self.gui,self)
        #loc = ToolLocus(self.gui,self)
        loc = ToolActor(self.gui,self)
        por = ToolPort(self.gui,self)
        DropDecorator(self, self.paste)
        return app
    def _create(self,x,y,comp = None):
        comp = self.spawn(x,y)
        self.items.append(comp)
        comp.local = NENHURES()
    def reshape(self, block):
        return (0,0)
    def paste(self,x,y,item):
        if item in self.items:
            return True
        #item.revert()
        
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

