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

class Composite(Item):
    """ Um item composto
    """
    def create(self):
        self.items =[]
        self._readjust()
        return self.icon
    def _noaction(self,*args):
        return False
    def _readjust(self):
        cx, cy = self.container.icon.pos()
        x, y = self.icon.pos()
        self.dxdy = (x-cx,y-cy)
    def _click(self,x,y):
        self.origin = self.xy
        xyz = zip ((x,y,x*y), PRIMESXYZ, (2,1,0))
        color = sum((ord * prime) % WHITE * WHITE**axis for ord, prime, axis in xyz)
        self._create(x,y,color)
    def adjust(self,x,y):
        dx, dy = self.dxdy
        self.avatar.move(x+dx,y+dy)
        self.xy = self.icon.pos()
        [item.adjust(x+dx,y+dy) for item in self.items]
    def revert(self):
        self._move(*self.origin)
        [item.revert() for item in self.items]
    def _start(self,x,y):
        print '>>',
        self.origin = self.xy = self.avatar.pos()
        [item._start(x,y) for item in self.items]
        self._readjust()
        return True
    def _move(self,x,y):
        print '.',
        self.avatar.move(x,y)
        self.xy = (self.avatar.pos())
        [item.adjust(x,y) for item in self.items]
        self._readjust()
    def paste(self,x,y,item):
        if item is self:
            self.container.reshape(self)
            return False
        if not item in self.items:
            item.revert()
            self._create(x,y,item.color)
            
        return True
    def _create(self,x,y,color):
        icon = self.gui.image(
            None, x, y, BLOCK_SIZE, BLOCK_SIZE, cl = '#%06x'%color)
        comp = Composite(self.gui,self,icon)
        DragDecorator(comp,action=comp._move,start=comp._start,stop=comp.paste)
        DropDecorator(comp,comp.paste)
        comp.origin, comp.xy, comp.size = (x,y), (x,y),(BLOCK_SIZE,)* 2
        comp.color = color
        #print 'comp.xy x, y = ',comp.xy, self
        self.items.append(comp)
        self.reshape(comp)
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

class App(Composite):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        self.items =[]
        self.xy = self.origin = (50,50)
        app = self.gui.text(350, 10, 'Jeppeto')
        self.icon = app = self.gui.image( None,50, 50, 700, 550, cl = '#FFDFB0')
        self.activate = self._click
        DropDecorator(self, self.paste)
        return app
    def reshape(self, block):
        return (0,0)
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

