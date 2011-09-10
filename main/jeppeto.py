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
import zipfile
from io import BytesIO
ICONS = zipfile.ZipFile('/home/carlo/shine-icon-set.zip', 'r')
ICO = file('/home/carlo/png/16x16/accept.png')

class JPObject(list):
    def __init__(self, gui, container = None, icon = None):
        self.gui = gui
        self.go = False
        self.icon = icon
        self.container = container
        self.avatar = self.create()
        self.gui.add_listener(self)
    def destroy(self):
        self.gui.remove_listener(self)
    def create(self):
        pass
    def create_child(self,icon):
        pass
    def click(self,x,y):
        print 'super',x,y
        pass
class JPClass(JPObject):
    def create(self):
        #self.gui.text(350, 70, 'JpClass',color='forest green')
        return self.icon #self.gui.rect(150, 150, 500, 100,color='forest green')
        pass
class Menu(JPObject):
    def create(self):
        #self.names = [x for x in ICONS.namelist() if ('16' in x) and ('.png' in x)]
        #self.menu = []
        #for ind, name in enumerate(self.names):
        #    f = ICONS.open(name).read()
        #    contents = BytesIO(f)
        #    x, y = 10+(ind // 20) * 20, 10+(ind % 20) * 20
        #    self.menu.append(
        #        self.gui.icon(name, x, y,16, 16, f='png', buff=contents))
        return self.gui.icon()

    def click(self,x,y):
        print 'go', self.go
        if self.go:
            self.icon = True
            self.go = False
            return
        if self.icon:
            #self.gui.clear()
            name, file = self.avatar.remove(x,y)
            self.container.create_child((name,file))
            self.icon = False
            self.go = True
            pass
     
class Jeppeto(JPObject):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self):
        self.gui.create_game(self, 'Jeppeto')
    def create(self):
        self.gui.text(350, 10, 'Jeppeto')
        jeppeto = self.gui.rect(50, 50, 700, 500)
        return jeppeto
    def click(self,x,y):
        if not self.go and self.avatar.collidepoint(x,y):
            print Jeppeto,x, y
            self.go = True
            self.menu = Menu(self.gui,self)
            self.menu.go = True
            #self.append(JPClass(self.gui, self))
    def create_child(self,icon):
        name, ico = icon
        icon = self.gui.image(name, 150, 150,128, 128, f='png', buff=ico)
        self.append(JPClass(self.gui, self,icon))
        self.menu.destroy()
        self.menu = None
    
def main():
    from pygame_factory import GUI
    main = Jeppeto(GUI())
    main.start()
    
if __name__ == "__main__":
    main()
