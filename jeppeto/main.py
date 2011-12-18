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

from gui_decorator import Item

class Composite(Item):
    """ Um item composto
    """
    def create(self):
        self.items =[]
        #self.activate = self._no_click
        return self.icon
    def _click(self,x,y):
        
        color = x*17% 256 *256*256 + y*19% 256*256  +(x*y*13)% 256
        self.reshape(x,y)
        icon = self.gui.image( None,x,y,50, 50, cl = '#%06x'%color)
        #self.gui.rect( x,y,50, 50,hexcolor='#%06x'%color, buff = icon.image)
        #icon = self.gui.rect( x,y,50, 50,hexcolor='#%06x'%color)
        #icon.move_ip(20,20)
        comp = Composite(self.gui,self,icon)
        comp.xy, comp.size = (x,y), (50,50)
        comp.color = color
        print 'comp.xy x, y = ',comp.xy, self
        self.items.append(comp)
        return True
    def reshape(self,x,y):
        print 'inflating', self.avatar
        self.container.reshape(x,y)
        x,y = self.xy
        w,h = self.size
        self.size = (w+50, h+50)
        self.avatar.scale(w+50,h+50)
        #self.avatar = self.gui.rect( x,y,w+50, h+50,hexcolor=self.color)
    def n_click_template(self,x,y):
        self.activate = self._no_click
        self._click(x, y)
    

class App(Composite):
    """ Engenho de Criação de Jogos educacionais
    """
    def start(self, name):
        self.gui.create_game(self, name)
    def create(self):
        self.items =[]
        app = self.gui.text(350, 10, 'Jeppeto')
        app = self.gui.rect(50, 50, 700, 500)
        self.activate = self._click
        return app
    def reshape(self,x,y):
        pass
    '''
    def _click(self,x,y):
        
            x,y = self.xy = (x,y)
            print 'self.xy x, y = ',self.xy
            color = x% 256 *256*256 + y% 256*256  +(x*y)% 256
            self.items.append(self.gui.rect( x,y,50, 50,hexcolor='#%06x'%color))
    def _click_template(self,x,y):
        #self.activate = self._no_click
        self._click(x, y)
    '''    
def main():
    from pygame_factory import GUI
    main = App(GUI())
    main.start('Jeppeto')
    
if __name__ == "__main__":
    main()

