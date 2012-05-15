#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Jeppeto : An Educational Game Builder
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/09/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/09/09 $Date$"
import logging

PRIMESXYZ = (5,11,111)
SATURATE = 256
FIELDS = 'items,color,origin'.split(',')

HEX6 = '#%06x'
BLACK, WHITE , GREY , NAVWHITE ='#000000', '#FFFFFF', '#A0A0A0', '#FFDFB0'
BLOCK_SIZE = 50
BP = BLOCK_PADDING = 10
X,Y = (0,1)

PASS = lambda *a, **kw: None
NULL_ELEMENT = type ('_Null_Element', (object,),dict(
    reshape = PASS, remove = PASS))

logger = logging.getLogger('jeppeto_main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.CRITICAL)
logger.setLevel(logging.DEBUG)

class ClickDecorator:
    def __init__(self, object, action = None, start = None, stop = None):
        self.action = action or self._no_action
        self.start = start or self._no_action
        self.stop = stop or self._no_action
        self.object = object
        self._action()
    def _action(self):
        self.object.gui.click(self)
    def _no_action(self, *args):
        return True
    def get_avatar(self):
        return self.object.avatar#.avatar
    def collide(self,x,y):
        #self.object.gui.talk('collide %s %s'%(x,y))
        return self.object.avatar.collidepoint(x,y)

class DragDecorator(ClickDecorator):
    def _action(self):
        self.object.gui.dragg(self)

class DropDecorator(ClickDecorator):
    def _action(self):
        self.object.gui.drop(self)
        

class GuiObject:#(list):
    def __init__(self, gui, container = None, icon = None, action = None):
        self.gui = gui
        self.activate = self._click_template
        self.container = container
        self.icon = icon
        self.clicker = ClickDecorator(self,self.click)
        self.avatar = self.icon = icon or self.create()
        self.action = action or self.create_child
    def get_avatar(self):
        return self.icon#.avatar
    def destroy(self):
        self.gui.unclick(self.clicker)
    def create(self):
        pass
    def click(self,x,y):
        self.activate(x,y)
        return True
    def _click(self,x,y):
        print 'super',x,y
    def _no_click(self,x,y):
        pass
    def _click_template(self,x,y):
        self.activate = self._no_click
        go = self._click(x, y)
        self.activate = self._click_template
        return go
    def create_child(self,icon):
        pass

class Menu(GuiObject):
    def create(self):
        self.activate = self._prepare
        return self.gui.icon()

    def _prepare(self,x,y):
        self.activate = self._click_template
    def _click(self,x,y):
        name, file = self.avatar.remove(x,y)
        self.action((name,file))

    def _click_template(self,x,y):
        self.activate = self._no_click
        self._click(x, y)
     
class Item(GuiObject):
    """ Engenho de Criação de Jogos educacionais
    """
    def create(self):
        return self.icon
    def _click(self,x,y):
        return
        if self.avatar.collidepoint(x,y):
            self.xy = (x,y)
            self.menu = Menu(self.gui,self,action=self.create_child)
    def create_child(self,icon):
        name, ico = icon
        x, y = self.xy
        print 'Item child with x, y = ',self.xy
        icon = self.gui.image(name, x,y,128, 128, f='png', buff=ico)
        model, action = self.action(self.container)
        self.append(Item(self.gui, model, icon=icon,action=action))
        self.menu.destroy()
        self.activate = self._click_template
class BlockItem(Item):
    """ Um bloco que arrasta e solta
    """
    def __init__(self, gui, container = None, icon = None):
        self.gui = gui
        self.container = container or NULL_ELEMENT
        self.xy = self.origin = (0,0)
        self.size = (BLOCK_SIZE,BLOCK_SIZE)
        self.items =[]
        self.element = NULL_ELEMENT
        self.avatar = self.icon = icon
        self.avatar = self.icon = self.create() or icon
        self.clicker = ClickDecorator(self,self.click)
    def create(self):
        return None
    def ncreate(self):
        self.xy = self.origin = (0,0)
        self.size = (BLOCK_SIZE,BLOCK_SIZE)
        self.items =[]
        self.element = NULL_ELEMENT #Elemento()
        #self.icon = self.icon or self.stereotype(*self.xy)
        return self.icon
    def to_front(self):
        self.icon.toFront()
        self.gui.toFront(self.clicker)
        [item.to_front() for item in self.items]
    def _noaction(self,*args):
        return False
    def translate(self,dx,dy):
        self.avatar.translate(dx,dy)
        self.xy = self.xy[X]+dx, self.xy[Y]+dy # self.icon.pos()
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
   
class Composable(BlockItem):
    """ Um item composto
    """
    def _click(self,x,y):
        self.origin = self.xy
        self._create(x,y)
    def _create(self,x,y, comp = None):
        comp = comp or self.spawn(x,y,self._colour(x,y))
        self.save(comp)
        self.items.append(comp)
        #print 'paste %s'%self.items
        comp.local = self
        self.reshape(comp)
    def paste(self,x,y,item):
        if item is self:
            logger.debug("rejecting self, %s , %s", self,  item)
            return False
        if not item in self.items:
            logger.debug("cloning self, %s , %s", self,  item)
            item.revert()
            self._create(x,y,comp = item.clone(x,y, owner = self))
            pass
        else:
            logger.debug("move instead of clone, %s , %s", self,  item)
            self.save(Mover(item, xy = [x,y]))
            #self.reshape(item)
        return True
        
    def _colour(self,x,y):
        xyz = zip ((x,y,x*y), PRIMESXYZ, (2,1,0))
        return sum((ordin * prime) % SATURATE * SATURATE**axis
            for ordin, prime, axis in xyz)
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
        #print 'spawned : %s'%color
        return comp
    def clone(self,x,y,color=None, owner = None):
        refcolor = color or self.clone_contents(x,y)
        color = self._colour(x, y)
        comp = Reference(self,self.stereotype(x,y,refcolor), owner, color = color)
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
    def extra(self): return {}
    def convert(self):
        d = dict(cls = self.__class__.__name__)
        d.update (dict ((field[:3], getattr(self,field))
            for field in FIELDS if hasattr(self,field) and getattr(self,field)))
        d.update (dict (('con', self.container.color)
            for field in ['container'] if hasattr(self,field) and getattr(self,field)))
        d.update(self.extra())
        return d
    def save(self,comp):
        pass       
    def load(self,owner, loader,its=[],col=0,ori=0,con=0,cls=0,ref=0):
        x, y = ori
        color = col
        elemento = self.spawn(x, y,color,owner=con)
        elemento.local = con #er
        owner.items.append(elemento)
        owner.reshape(elemento)
        return elemento
    def clone_contents(self,x,y):
        return self.color or self._colour(x,y)
    def receber(self, elemento, ato):
        x, y = self.icon.pos()
        #elemento.icon.toFront()
        elemento.to_front()
        elemento._move(x+BP,y+BP)
        elemento.container = self
        self.reshape(elemento)


class ToolBox(Composable):
    """ Caixa de ferramentas de edição
    """
    def reverter(self,x,y,item):
        item.revert()
    def delete(self):pass
    def clone(self,x,y,color=None, owner = None):
        return self.spawn(x,y,color,owner = owner)
    """ Tool
    """
    def n__init__(self, gui):
        self.gui = gui
        self.xy = (750, 250)
    def create(self):
        self.xy = (750, 250)
    def build(self, tool, xy = None):
        if not xy:
            x, y = xy = self.xy
            self.xy = x, y - 50
        tool.paste = self.reverter
        tool.clone = tool.spawn
        tool.delete = self.delete
        tool.color = None           
        tool.icon = tool.avatar = tool.icon or tool.stereotype(0,0)
        tool.icon.scale(BLOCK_SIZE-10,BLOCK_SIZE-10)
        tool.icon.move(*xy)
        DragDecorator(tool,action=tool._move,start=tool._start,stop=tool.paste)
        return tool
     
class App(ToolBox):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        app = self.gui.text(350, 10, 'Jeppeto')
        app = self.gui.rect(50, 50, 700, 500)
        return app
    def _click(self,x,y):
        
            self.xy = (x,y)
            print 'self.xy x, y = ',self.xy
            self.menu = Menu(self.gui,self,action=self.create_child)
    def _click_template(self,x,y):
        self.activate = self._no_click
        self._click(x, y)
    
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()
