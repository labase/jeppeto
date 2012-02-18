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
import json

JE = json.JSONEncoder()
PRIMESXYZ = (5,11,111)
SATURATE = 256
FIELDS = 'items,color,origin'.split(',')

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
    ########### should move to Null Composite ############
    def reshape(self, *args):
        pass
    def remove(self, *args):
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
    def extra(self):
        return {}
        

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
        for item in self.items:
            if item.entra(ato):
                return True
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
    def entra(self,ato): 
        print 'Portal entrou'
        for item in self.items:
            if item.age(ato):
                return True
        did = self.local.age(ato or self.agir)
        return did
       
class Referencia(Elemento):
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
#def NOSAV(it): pass
   
class Composite(BlockItem):
    """ Um item composto
    """
    #SAVER = NOSAV
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
            print "rejecting self", self,  item
            return False
        if not item in self.items:
            print "cloning", self, item
            item.revert()
            self._create(x,y,comp = item.clone(x,y, owner = self))
            pass
        else:
            print "move instead of clone", self, item
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
        #print 'default(', repr(obj), ')'
        # Convert objects to a dictionary of their representation
        d = dict(
              cls = self.__class__.__name__, 
              )
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
    def __init__(self, referee = None, icon = None, owner = None, gui = None, color =0):
        self.referee = referee
        Referencia.__init__(self,referee)
        agui = gui  or owner.gui
        Composite.__init__(self,agui,owner,icon)
        self.gui.rect(0,0,24,24,hexcolor=BLACK,buff=self.icon.image)
        self.gui.rect(2,2,20,20,hexcolor=color,buff=self.icon.image)
    def _create(self,x,y, comp = None):
        pass
    def paste(self,x,y,item):
        if item is self:
            return False
        else:
            item.revert()
        return True
    def stereotype(self,x,y,color):
        icon = self.referee.stereotype(x,y,self.referee.color)
        self.gui.rect(0,0,4,4,hexcolor=WHITE,buff=icon.image)
        return icon
    def clone(self,x,y,color=None, owner = None):
        ref = self.referee
        refcolor = ref.color
        color = color or self._colour(x, y)
        comp = Reference(ref,self.stereotype(x,y,refcolor), owner, color = color)
        return self._spawn(x,y,comp,color)
    def adentra(self,local):
        pass
    def extra(self):
        return dict(ref=self.referee.color)
    def load(self,owner, loader,its=[],col=0,ori=0,con=0,cls=0,ref=0):
        x, y = ori
        color = col
        self.referee = loader.element_pool(ref)
        elemento = self.clone(x, y,color,owner=owner)
        elemento.local = owner
        owner.items.append(elemento)
        owner.reshape(elemento)
        return elemento
    
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

class Deleter(Reference):
    def __init__(self, referee = None, icon = None, owner = None, gui = None):
        self.referee = referee
        if referee: referee.delete()
    def load(self,owner, loader,its=[],col=0,ori=0,con=0,cls=0,ref=0):
        self.referee = loader.element_pool(ref)
        return Deleter(self.referee)
    def delete(self):
        del self

class Mover(Deleter):
    def __init__(self, referee = None, icon = None,
                 owner = None, gui = None, xy = [0,0]):
        self.referee = referee
        x, y, = self.origin = xy
        if referee:
            referee._move(x,y)
            if referee.container:
                referee.container.reshape(referee)
    def load(self,owner, loader,its=[],col=0,ori=0,con=0,cls=0,ref=0):
        self.referee = loader.element_pool(ref)
        return Mover(self.referee, xy = ori)

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
        dlt = Deleter(item)
        self.save(dlt)
        return True

class App(Locus):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        self.items =[]
        Loader(self)
        App.SINK = file('jpt.jpt','a')
        Composite.save = self.saver
        #App.SINK.write('[')
        self.gui.cleanup = self.cleanup
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
    def cleanup(self):
        #App.SINK.write('{}]')
        #saver(self.items)
        App.SINK.close()
        
    def _create(self,x,y,comp = None):
        comp = self.spawn(x,y)
        self.save(comp)
        self.items.append(comp)
        print 'created from App'
        comp.local = NENHURES()
    def reshape(self, block):
        return (0,0)
    def paste(self,x,y,item):
        if item in self.items:
            self.save(Mover(item, xy = [x,y]))
            return True
        #item.revert()
    def saver(self, block):
        #App.SINK.write(json.dumps(block, indent=2, default=convert_to_builtin_type)+',')
        App.SINK.write(json.dumps(block, indent=2, default= lambda o: o.convert())+',')
        App.SINK.flush()

class Loader:
    def __init__(self, owner):
        App.SINK = file('jpt.jpt','r')
        json_string = App.SINK.read()
        if len(json_string) < 4: return
        
        json_string = '['+ json_string[:-1]+']'
        #print json_string[-20:]
        CLASS_DICT={}
        self.ELEMENT_DICT={-1:owner}
        python_object_list = []
        icon = owner.gui.image( None,-100, -100, 1, 1, cl = '#FFDFB6')
        try:
            python_object_list = json.loads(json_string)
        except:
            raise Exception("Problem reading from JSON stream")
        def flyweight(clazz):
            if clazz in CLASS_DICT:
                return CLASS_DICT[clazz]
            else:
                cl = CLASS_DICT[clazz] = globals()[clazz](gui = owner.gui, icon=icon)
                return cl
        def instantiate(python_object,its=[],col=0,ori=0,con=0,cls=0,ref=0):
            clazz = flyweight(cls)
            owner = self.element_pool(con or -1)
            container_nowhere_when_app = not con and NENHURES() or owner
            python_object['con']= container_nowhere_when_app
            #print 'owner', own, owner
            element = clazz.load(owner,self,**python_object)
            #print 'element',element
            self.element_pool(col, element)
        [instantiate(po,**po) for po in python_object_list if po]
        App.SINK.close()
        #for cls, instance in CLASS_DICT.items() : instance.delete()
    def element_pool(self,name,clazz=None):
        if name in self.ELEMENT_DICT:
            return self.ELEMENT_DICT[name]
        else:
            cl = self.ELEMENT_DICT[name] = clazz
            return cl
        
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

