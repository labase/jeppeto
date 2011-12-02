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


class ClickDecorator:
    def __init__(self, object, action = None):
        self.action = action
        self.object = object
        object.gui.click(self)
    def collide(self,x,y):
        return self.object.avatar.collidepoint(x,y)

class GuiObject(list):
    def __init__(self, gui, container = None, icon = None, action = None):
        self.gui = gui
        self.activate = self._click_template
        self.icon = icon
        self.container = container
        self.avatar = self.create()
        self.action = action or self.create_child
        self.clicker = ClickDecorator(self,self.click)
    def destroy(self):
        self.gui.unclick(self.clicker)
    def create(self):
        pass
    def click(self,x,y):
        self.activate(x,y)
    def _click(self,x,y):
        print 'super',x,y
    def _no_click(self,x,y):
        pass
    def _click_template(self,x,y):
        self.activate = self._no_click
        self._click(x, y)
        self.activate = self._click_template
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

class Tool(Item):

    def _click(self,x,y):
            self.xy = (x,y)
            self.drag = Menu(self.gui,self,action=self.create_child)
     
class App(Item):
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
