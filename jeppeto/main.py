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
WHITE = 256
BLOCK_SIZE = 50
BP = BLOCK_PADDING = 10
X,Y = (0,1)

NENHURES = None
NINGUEM = None
NADA = None

class Elemento:
    """ Um elemento básico do Jogo.
    """
    TEMPO = 0
    def __init__(self, inicial =[]):
        """ inicia a posição e a imagem
        """
        self.local = NENHURES
        self.items =[]
        self.agir = self.move
        self._inicia()
    def _inicia(self):
        [inicia() for inicia in inicial]
    def age(self,*args):
        self.local.age(self.agir)
    def move(self,local):
        local.recebe(self.local.devolve(self))
    def adentra(self,local):
        self.local = local
    def recebe(self,elemento):
        return local
    def devolve(self,elemento):
        return elemento
       
class Local(Elemento):
    """ Um local onde se pode colocar Elementos
    """
    def recebe(self,elemento):
        if not elemento in self.items:
            self.items.append(elemento)
            elemento.adentra(self)
    def devolve(self,elemento):
        self.items.remove(elemento)
        return elemento

class Portal(Elemento):
    """ Um portal de passagens entre locais
    """
    def _inicia(self):
        self.de = NENHURES
        self.para = NENHURES
        [inicia() for inicia in inicial]
    def recebe(self,elemento):
        [item.recebe(elemento) for item in self.items]
        return self
    def devolve(self,elemento):
        return elemento

class Atividade(Elemento):
    """ Um comportamento que pode ser atribuido a um elemento ou local
    """
    def _inicia(self):
        pass


class Composite(Item):
    """ Um item composto
    """
    def create(self):
        self.xy = self.origin = (0,0)
        self.size = (BLOCK_SIZE,BLOCK_SIZE)
        self.items =[]
        return self.icon
    def _noaction(self,*args):
        return False
    def _click(self,x,y):
        self.origin = self.xy
        xyz = zip ((x,y,x*y), PRIMESXYZ, (2,1,0))
        color = sum((ord * prime) % WHITE * WHITE**axis for ord, prime, axis in xyz)
        self._create(x,y,color)
    def translate(self,dx,dy):
        self.avatar.translate(dx,dy)
        self.xy = self.icon.pos()
        [item.translate(dx,dy) for item in self.items]
    def revert(self):
        self._move(*self.origin)
        [item.revert() for item in self.items]
    def _start(self,x,y):
        print '>>',
        self.origin = self.xy = self.avatar.pos()
        [item._start(x,y) for item in self.items]
        return True
    def _move(self,x,y):
        print '.',
        dx, dy = x - self.xy[X], y - self.xy[Y]
        self.translate(dx, dy)
    def paste(self,x,y,item):
        if item is self:
            #self.container.reshape(self)
            return False
        if not item in self.items:
            item.revert()
            self._create(x,y,comp = item.clone(x,y, owner = self))
            pass
        else:
            self.reshape(item)
            
            
        return True
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
    
    def clone(self,x,y,color=None, owner = None):
        thecolor = color or self.color
        comp = self.stereotype(x,y,thecolor,owner)
        DragDecorator(comp,action=comp._move,start=comp._start,stop=comp.paste)
        DropDecorator(comp,comp.paste)
        comp.origin, comp.xy, comp.size = (x,y), (x,y),(BLOCK_SIZE,)* 2
        comp.color = thecolor
        return comp
    def _create(self,x,y,color = 0xFFFFFF, comp = None):
        comp = comp or self.clone(x,y,color)
        self.items.append(comp)
        self.reshape(comp)
    def stereotype(self,x,y,thecolor, owner = None):
        icon = self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = '#%06x'%thecolor)
        self.gui.rect(0,0,BLOCK_SIZE,2,hexcolor='#000000',buff=icon.image)
        return Composite(self.gui,owner or self,icon)
        
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

class Locus(Composite,Local):
    """ Portal
    """
    def stereotype(self,x,y,color, owner = None, it = None, icon = None):
        color = 0xFFAAAA
        icon =  icon or self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = '#%06x'%color)
        self.gui.rect(0,0,2,BLOCK_SIZE,hexcolor='#000000',buff=icon.image)
        container = owner or self.container
        return it or Locus(self.gui, container, icon)
    def _click(self,x,y):
        pass
    
class Port(Locus,Portal):
    """ Portal
    """
    def stereotype(self,x,y,color, owner = None, it = None, icon = None):
        color = 0xAAAAFF
        icon = icon or self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = '#%06x'%color)
        self.gui.rect(BLOCK_SIZE-2,0,2,BLOCK_SIZE,hexcolor='#000000',buff=icon.image)
        container = owner or self.container
        comp = it or Port(self.gui, container, icon)
        return comp
    """
    """
class Tool():
    """ Tool
    """
    def paste(self,x,y,item):
        print 'tool reverting'
        item.revert()
    def delete(self):pass
    
class ToolPort(Tool,Port):
    """ Ferramenta de Portal
    """
    def create(self):
        DragDecorator(self,action=self._move,start=self._start,stop=self.paste)
        self.color = 0xAAAAFF
        self.icon = self.gui.image(
            None, 750, 250, BLOCK_SIZE-10, BLOCK_SIZE-10, cl = '#%06x'%self.color)
        self.gui.rect(BLOCK_SIZE-12,0,2,BLOCK_SIZE,hexcolor='#000000',buff=self.icon.image)
        self.stereotype(750, 250, self.color, icon = self.icon, it = self)
        self.items =[]
        return self.icon

class ToolLocus(Tool,Locus):
    """ Ferramenta de Locus
    """
    def create(self):
        DragDecorator(self,action=self._move,start=self._start,stop=self.paste)
        self.color = 0xFFAAAA
        self.icon = self.gui.image(
            None, 750, 200, BLOCK_SIZE-10, BLOCK_SIZE-10, cl = '#%06x'%self.color)
        self.gui.rect(0,0,2,BLOCK_SIZE,hexcolor='#000000',buff=self.icon.image)
        self.stereotype(750, 200, self.color, icon = self.icon, it = self)
        self.items =[]
        return self.icon

class DustBin(Composite):
    """ Lata de lixo
    """
    def create(self):
        RR=3
        DropDecorator(self, self.scrap)
        self.icon = self.gui.image(
            None, 750, 430, BLOCK_SIZE-10, BLOCK_SIZE-10, cl = '#FFDFB0')
        self.gui.rect(10,0,20,RR,hexcolor='#A0A0A0',buff=self.icon.image)
        self.gui.rect(2,RR,BLOCK_SIZE-14,BLOCK_SIZE-14,hexcolor='#A0A0A0',buff=self.icon.image)
        self.gui.rect(RR+8,RR+4,2,BLOCK_SIZE-24,hexcolor='#FFDFB0',buff=self.icon.image)
        self.gui.rect(RR+16,RR+4,2,BLOCK_SIZE-24,hexcolor='#FFDFB0',buff=self.icon.image)
        self.gui.rect(RR+24,RR+4,2,BLOCK_SIZE-24,hexcolor='#FFDFB0',buff=self.icon.image)
        self.gui.rect(0,RR+4,BLOCK_SIZE,2,hexcolor='#FFDFB0',buff=self.icon.image)
        self.gui.unclick(self)
        return self.icon
    def scrap(self,x,y,item):
        print "scrapping %s"%item
        item.delete()
        return True

class App(Composite):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        self.items =[]
        self.xy = self.origin = (0,0)
        app = self.gui.text(350, 10, 'Jeppeto', hexcolor = '#FFDFBF')
        self.icon = app = self.gui.image( None,0, 0, 750, 600, cl = '#FFDFB6')
        self.activate = self._click
        comp = DustBin(self.gui,self)
        loc = ToolLocus(self.gui,self)
        por = ToolPort(self.gui,self)
        DropDecorator(self, self.paste)
        return app
    def reshape(self, block):
        return (0,0)
    #def paste(self,x,y,item):
    #    item.revert()
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

